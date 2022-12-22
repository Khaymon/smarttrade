from stock_data import StockData, StocksList
from models import MODELS_DICT
from targets.functions import TARGETS_DICT
from config import Config

import argparse
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

def main():
    args = parse_arguments()
    
    config = Config(args.config_file)
    
    assert config.model_name in MODELS_DICT, f"{config.model_name} is not a model"
    assert config.target_function in TARGETS_DICT, f"{config.target_function} is not a target functions"
    
    model = MODELS_DICT[config.model_name](**config.model_args)
    target_function = TARGETS_DICT[config.target_function](**config.target_function_args)

if __name__ == "__main__":
    main()