import os
import pandas as pd

with open("data/path.conf", "r", encoding="utf-8") as f:
    paths = [line.strip() for line in f if line.strip()]

for path in paths:
    if not os.path.exists(path):
        print(f"File not found: {path}")
        continue

    df = pd.read_csv(path)

    df = df.drop(columns=["Unnamed: 0"], errors="ignore")

    df = df.rename(
        columns=lambda x: (
            "name"
            if pd.Series(x).str.contains("(?i)name").any() or x == ""
            else x
        )
    )

    if "id" not in df.columns:
        df.insert(0, "id", range(0, len(df)))
    else:
        id_col = df.pop("id")
        df.insert(0, "id", id_col)

    df.to_csv(path, index=False)
    print(f"File {path} is ready.")
