import pandas as pd

data = open("data/path.conf").read().split("\n")

for i in data:
    df = pd.read_csv(i)
    df['id'] = range(0, len(df))
    try:
        df = df.drop(columns=['Unnamed: 0'])
    except:
        pass
    df.to_csv(i, index=False)

