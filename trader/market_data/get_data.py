import json
import datetime
import time
import re
from typing import List
import os

import requests
from tqdm import tqdm
import pandas as pd

# Timeout in seconds before next try to get the data
TIMEOUT = 20

# Base URL to get the market data
BASE_URL = "https://api.polygon.io/v2/aggs/ticker/{TICKER}/range/{INTERVAL}/" +\
           "{RANGE}/{FROM_DATE}/{TO_DATE}?limit=50000&apiKey={API_KEY}"


def get_url(token: str, interval_len: int, interval: str, from_date: datetime.date, to_date: datetime.date,
            api_key: str):
    """
    Constructs the URL from the base URL to get a data
    """
    url = re.sub("{TICKER}", token, BASE_URL)
    url = re.sub("{INTERVAL}", str(interval_len), url)
    url = re.sub("{RANGE}", interval, url)
    url = re.sub("{FROM_DATE}", str(from_date), url)
    url = re.sub("{TO_DATE}", str(to_date), url)
    url = re.sub("{API_KEY}", api_key, url)

    return url


def get_ticker_data(ticker: str, time_interval: int, time_units: str,
                    start_date: datetime.date, finish_date: datetime.date, api_key: str):
    current_date = start_date
    data_frames = []
    while current_date < finish_date:
        request_url = get_url(ticker, time_interval, time_units, current_date, finish_date, api_key)
        data = requests.get(url=request_url)
        if data.json()["status"] == "ERROR":
            print("Waiting for", TIMEOUT, "seconds")
            for _ in tqdm(range(TIMEOUT)):
                time.sleep(1)
        else:
            if "results" in data.json().keys():
                current_df = pd.DataFrame(data.json()["results"])
            else:
                continue
            next_date = (pd.Timestamp(current_df["t"].max(), unit="ms") + pd.DateOffset(days=1)).date()
            print(f"Get DataFrame of {ticker} with shape {current_df.shape} from {current_date} to {next_date}")
            current_date = next_date

            data_frames.append(current_df)

    result_df = pd.concat(data_frames)
    result_df.drop_duplicates(inplace=True)

    return result_df


def get_data(config_data: dict):
    data_frames = []
    for ticker in config_data["tickers"]:
        data = get_ticker_data(
            ticker=ticker,
            time_interval=config_data["time_interval"],
            time_units=config_data["time_units"],
            start_date=pd.Timestamp(config_data["start_date"]).date(),
            finish_date=pd.Timestamp(config_data["finish_date"]).date(),
            api_key=config_data["api_key"]
        )

        data["t"] = data["t"].apply(lambda row: pd.Timestamp(row, unit="ms"))
        data["ticker"] = ticker
        data_frames.append(data)

    assert len(data_frames) == len(config_data["tickers"])

    result_df = pd.concat(data_frames)
    result_df.drop(["vw", "n"], axis=1, inplace=True)
    result_df.rename({
        "v": "volume",
        "o": "open",
        "c": "close",
        "h": "high",
        "l": "low",
        "t": "date"
    }, axis=1, inplace=True)
    result_df.reset_index(drop=True, inplace=True)

    return result_df


if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)

    data_frames = get_data(config_data)

    dataset_path = os.path.join("./datasets", config_data["dataset_name"]) + ".csv"
    data_frames.to_csv(dataset_path)
