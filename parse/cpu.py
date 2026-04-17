import requests
from bs4 import BeautifulSoup
import pandas as pd
import os.path
from logger import log

data = pd.DataFrame(columns=["cpuName", "cpuValue", "price", "cpuMark", "TDP", "cores", "threads", "maxSpeed", "socket", "category", "brnd", "link"])
domen = "https://www.cpubenchmark.net"
all_cpu = "https://www.cpubenchmark.net/cpu_value_available.html"

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

response = requests.request("GET", all_cpu, headers=headers, data=payload).text

soup = BeautifulSoup(response, 'lxml')

names = soup.find_all('span', class_='prdname')
prices = soup.find_all('span', class_='price-neww')
values = soup.find_all('span', class_='count')
cpuMark = soup.find_all('span', class_='mark-neww')

lnks = []
for a in soup.find_all('a'):
    try:
        if "cpu.php?" in str(a['href']): 
            lnks.append(a['href'])
    except: pass
ids = len(names)
ids = 10

for i in range(0, ids):
    data.loc[i, "cpuName"] = names[i].text
    data.loc[i, "link"] = domen + lnks[i]
    data.loc[i, "price"] = float(prices[i].text.replace("$", ""))
    data.loc[i, "cpuValue"] = float(values[i].text)
    data.loc[i, "cpuMark"] = cpuMark[i].text

    
    if "Intel" in str(names[i]):
        data.loc[i, "brnd"] = "INTEL"
    elif "AMD" in str(names[i]):
        data.loc[i, "brnd"] = "AMD"
    else:
        data.loc[i, "brnd"] = "Other"


if not os.path.exists("preCPU.csv"):
    for i in range(0, ids):
        lnk = data["link"][i]
        log(f"Search CPU {i+1}/{ids} {data["cpuName"][i]}")
        try:
            response_t = requests.request("GET", lnk, headers=headers, data=payload).text
            soup_t = BeautifulSoup(response_t, "lxml")
        except Exception as e:
            log(f"Server closed connection: {e}")
            exit()

        # DESCRIPTION RIGHT
        desc = soup_t.find_all('div', class_="right-desc")[0]

        sthread_rating = desc.find('span', style=lambda value: value and 'font-size: 44px' in value)

        # DESCRIPTION LEFT
        desc_l = soup_t.find_all('div', class_="left-desc-cpu")[0]

        tdp = desc_l.find('strong', string="Typical TDP:")
        if tdp and tdp.next_sibling:
            max_tdp = int(tdp.next_sibling.strip().replace('W', ''))
        
        category_label = desc_l.find('strong', string="Class:")
        if category_label and category_label.next_sibling:
            category = category_label.next_sibling.strip()

        socket_label = desc_l.find('strong', string="Socket:")
        if socket_label and socket_label.next_sibling:
            socket = socket_label.next_sibling.strip()

        max_speed = desc_l.find('strong', string="Turbo Speed:")
        if max_speed and max_speed.next_sibling:
            speed = max_speed.next_sibling.strip()

        cores_label = desc_l.find('strong', string="Cores:")
        if cores_label and cores_label.next_sibling:
            cores = cores_label.next_sibling.strip()

        threads_label = desc_l.find('strong', string="Threads:")
        if threads_label and threads_label.next_sibling:
            threads = threads_label.next_sibling.strip()

        if cores:
            log(f"Cores: {cores}")
            data.loc[i, "cores"] = int(cores)
        if threads:
            log(f"Threads: {threads}")
            data.loc[i, "threads"] = int(threads)
        if max_tdp:
            log(f"TDP: {max_tdp}")
            data.loc[i, "TDP"] = int(max_tdp)
        if speed:
            log(f"Max Speed: {speed}")
            data.loc[i, "maxSpeed"] = speed
        if socket:
            log(f"Socket: {socket}")
            data.loc[i, "socket"] = socket.replace("FCLGA", "LGA ")
        if category:
            log(f"Category: {category}")
            data.loc[i, "category"] = category

    data.to_csv("preCPU.csv")
else:
    data = data = pd.read_csv("preCPU.csv",)
    del data['Unnamed: 0']

print(data)