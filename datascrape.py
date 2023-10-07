
import os
import pandas as pd
import json
from urllib.request import urlretrieve
import datetime as dt

def fetch_data():
    url = "https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/nakamura_1979_sm_locations.csv"
    out_path = os.path.join("data", "nakamura", "nakamura_1979.csv")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    urlretrieve(url, out_path)

def convert_data_to_json():
    cols = ["yr", "doy", "hr", "min", "sec", "lat", "lng", "mag", "comment"]
    in_path = os.path.join("data", "nakamura", "nakamura_1979.csv")
    df = pd.read_csv(in_path, names=cols, header=0)

    df["date"] = pd.to_datetime(df["yr"] * 1000 + df["doy"], format="%Y%j")
    df["time"] = df.apply(lambda x: dt.time(x["hr"], x["min"], x["sec"]), axis=1)
    df["date"] = (pd.to_datetime(df["date"].astype(str) + " " + df["time"].astype(str))).astype(str)

    df = df.drop(index=14)
    df = df.drop(["yr", "doy", "hr", "min", "sec", "comment", "time"], axis=1)
    df["label"] = "Nakamura (1979)"

    out_path = os.path.join("data", "nakamura", "nakamura_1979.json")
    with open(out_path, "w") as out_file:
        out_file.write(json.dumps(df.to_dict("records"), indent=4))

if __name__ == "__main__":
    fetch_data()
    convert_data_to_json()
