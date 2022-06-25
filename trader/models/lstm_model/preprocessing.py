import json
from typing import List
import os
import pickle

import pandas as pd


def create_dataset(data: pd.DataFrame, time_interval: int, time_units: str,
                   window: int, date_column: str) -> List[pd.DataFrame]:
    """
    Creates dataset of sequential bars with time_interval lag
    """
    time_diffs = data[date_column].diff(window)

    train_data = []
    for idx, time_lag in enumerate(time_diffs):
        if time_lag == pd.Timedelta(value=time_interval, unit=time_units) * window:
            train_data.append(data[idx-window:idx])

    return train_data


def create_dataset_from_config(config_data: dict) -> List[pd.DataFrame]:
    result_train_dataset = []
    for dataset_name in config_data["datasets"]:
        dataset_path = os.path.join("../../market_data/datasets", dataset_name) + ".csv"

        raw_dataset = pd.read_csv(dataset_path, parse_dates=[config_data["date_column"]], index_col=0)
        result_train_dataset += create_dataset(
            data=raw_dataset,
            time_interval=config_data["time_interval"],
            time_units=config_data["time_units"],
            window=config_data["window"],
            date_column=config_data["date_column"]
        )

    print(f"Result dataset length: {len(result_train_dataset)}")

    return result_train_dataset


if __name__ == "__main__":
    with open("config.json", "rb") as config_file:
        config_data = json.load(config_file)

    train_data = create_dataset_from_config(config_data)

    train_dataset_path = os.path.join("../train_datasets", config_data["result_name"]) + ".pkl"
    with open(train_dataset_path, "wb") as output_file:
        pickle.dump(train_data, output_file)
