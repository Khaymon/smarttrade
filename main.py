from stock_data import StockData, StocksList
from stock_data import StocksDataTask

from models import MODELS_DICT
from targets.functions import TARGETS_DICT
from metrics import METRICS

from config import Config

import argparse
import re
import json
import os


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="Trading Algorithms",
        description="ML algorithms for stock market trading"
    )
    parser.add_argument("--config_file", dest="config_file", default="config.json",
                        help="Config file path", type=str)
    
    return parser.parse_args()

def get_tickers_from_dir(path: str):
    tickers_list = []

    for file_name in os.listdir(path):
        ticker = re.findall("([A-Z\-a-z]+).csv", file_name)
        tickers_list += ticker
        
    return tickers_list

def main():
    args = parse_arguments()
    
    config = Config(args.config_file)
    
    assert config.model_name in MODELS_DICT, f"{config.model_name} is not a model"
    assert config.target_function in TARGETS_DICT, f"{config.target_function} is not a target functions"
    
    model = MODELS_DICT[config.model_name](**config.model_args)
    target_function = TARGETS_DICT[config.target_function](**config.target_function_args)
    metric_function = METRICS[config.metric]
    
    if config.tickers == "ALL":
        tickers = get_tickers_from_dir(config.data_path)
    else:
        tickers = config.tickers
    
    stocks_list = StocksList.from_tickers_list(tickers, config.data_path)
    targets_list = target_function(stocks_list)
    
    task_data = StocksDataTask(stocks_list, targets_list)
    
    train_data, test_data = task_data.split(0.8)
    
    X_train, y_train = model.sampler.sample(train_data)
    X_test, y_test = model.sampler.sample(test_data)
    
    model.fit(X_train, y_train, **config.model_train_args)
    predictions = model.predict(X_test)
    
    metric = metric_function(y_test, predictions)
    print(f"{config.metric} = {metric}")

if __name__ == "__main__":
    main()