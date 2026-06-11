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


cpu_df = pd.read_csv("data/CPU.csv")
mb_df = pd.read_csv("data/MB.csv")

if "ramType" in cpu_df.columns:
    cpu_df = cpu_df.drop(columns=["ramType"])

cpu_df.insert(len(cpu_df.columns), "ramType", "None")

merged = cpu_df.reset_index().merge(
    mb_df[["socket", "ramType"]], on="socket", suffixes=("_cpu", "_mb")
)

ram_mapping = (
    merged.groupby("index")["ramType_mb"]
    .apply(lambda x: "/".join(sorted(x.unique())))
)

updated_ram = cpu_df.index.map(ram_mapping).to_series()
updated_ram.index = cpu_df.index
cpu_df["ramType"] = updated_ram.fillna(cpu_df["ramType"])

cpu_df.to_csv("data/CPU.csv", index=False)

# TODO Add filter by type of DDR
# TODO PSU data check id - 288 289 290