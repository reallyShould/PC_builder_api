import requests
from bs4 import BeautifulSoup
import pandas as pd
import os.path
from logger import log

data = pd.DataFrame(columns=["id", "gpuName", "G3Dmark", "G2Dmark", "price", "gpuValue", "TDP", "category", "brnd", "link"]) # MORE INFO... IN FUTURE
domen = "https://www.videocardbenchmark.net/"
all_cards = "https://www.videocardbenchmark.net/high_end_gpus.html"

payload = {}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://www.videocardbenchmark.net/',
    'Connection': 'keep-alive',
    'Cookie': 'PHPSESSID=2cbg5c5ec4rgg5t1st4nog2qct',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0, i'
}

response = requests.request("GET", all_cards, headers=headers, data=payload).text

soup = BeautifulSoup(response, 'lxml')

names = soup.find_all('span', class_='prdname')
prices = soup.find_all('span', class_='price-neww')
lnks = []
for a in soup.find_all('a'):
    if "gpu.php?" in str(a['href']): 
        lnks.append(a['href'])
ids = len(names)

for i in range(0, ids):
    data.loc[i, "gpuName"] = names[i].text
    data.loc[i, "link"] = domen + lnks[i]
    data.loc[i, "price"] = prices[i].text
    ## Need fixes
    if "GeForce" in str(names[i]) or "RTX" in str(names[i]) or "Quadro" in str(names[i]) or "NVIDIA" in str(names[i]):
        data.loc[i, "brnd"] = "NVIDIA"
    elif "Radeon" in str(names[i]) or "AMD" in str(names[i]) or "Ryzen" in str(names[i]) or "FirePro" in str(names[i]):
        data.loc[i, "brnd"] = "AMD"
    else:
        data.loc[i, "brnd"] = "Other"

tmp = 0
for i in range(0, ids):
    if "NA" in str(data["price"][i]):
        data = data.drop(index=[i])
    else:
        data.loc[i, "id"] = tmp
        tmp += 1
        
ids = len(data)

data["category"] = data["category"].astype(str)

if not os.path.exists("preGPU.csv"):
    for i in range(0, ids):
        lnk = data["link"][i]
        log(f"Search GPU {i+1}/{ids} {data["gpuName"][i]}")

        response_t = requests.request("GET", lnk, headers=headers, data=payload).text
        soup_t = BeautifulSoup(response_t, "lxml")

        # DESCRIPTION RIGHT
        desc = soup_t.find_all('div', class_="right-desc")[0]

        g3d_mark = desc.find('span', style=lambda value: value and 'font-size: 44px' in value)
        g2d_mark_label = desc.find('strong', string="Average G2D Mark:")

        # DESCRIPTION LEFT
        desc_l = soup_t.find_all('em', class_="left-desc-cpu")[0]

        tdp = desc_l.find('strong', string="Max TDP:")
        if tdp and tdp.next_sibling:
            max_tdp = int(tdp.next_sibling.strip().replace('W', ''))

        # DESC FOOTER
        footer = soup_t.find('div', class_="desc-foot")

        if footer:
            category_label = footer.find('p', string=lambda value: value and "Videocard Category:" in value)
            
            if not category_label:
                category_label = footer.find('p')
                strong_tag = category_label.find('strong', string="Videocard Category:")
                if strong_tag and strong_tag.next_sibling:
                    category = strong_tag.next_sibling.strip()
                    data.loc[i, "category"] = str(category)
                    
        log(f"Category: {category}")

        if g3d_mark:
            log(f"G3D Mark: {g3d_mark.text}")
            data.loc[i, "G3Dmark"] = int(g3d_mark.text)
        if g2d_mark_label:
            g2d_mark = g2d_mark_label.next_sibling.strip()
            data.loc[i, "G2Dmark"] = int(g2d_mark)
            log(f"G2D Mark: {g2d_mark}")
        if max_tdp:
            data.loc[i, "TDP"] = int(max_tdp)
            log(f"TDP: {max_tdp}")
    data.to_csv("preGPU.csv")
else:
    data = data = pd.read_csv("preGPU.csv",)
    del data['Unnamed: 0']

tmp = []
for i in range(data.__len__()): # JUST EXAMPLE INSERT #TODO Check it
    data["price"].values[i] = float(data["price"].values[i].replace(",", "").replace("*", ""))
    data.loc[i, "gpuValue"] = data["G3Dmark"].values[i] / data["price"].values[i]
    if data["category"].values[i] != 'Desktop':
        tmp.append(i)
    
data = data.drop(tmp, axis=0)
data = data.sort_values(by='gpuValue', ascending=False).reset_index(allow_duplicates=False)
del data['index']
del data['id']
data = data.drop_duplicates()

data.to_csv("GPU.csv")
