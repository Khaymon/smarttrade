import os
import json
from typing import Dict

MODEL_NAME_FIELD = "model_name"
MODEL_ARGS_FIELD = "model_args"
MODEL_TRAIN_ARGS_FIELD = "model_train_args"
TARGET_FUNCTION_FIELD = "target_function"
TARGET_FUNCTION_ARGS_FIELD = "target_function_args"
DATA_PATH_FIELD = "data_path"
TICKERS_FIELD = "tickers"


class Config:
    def __init__(self, config_path: str) -> None:
        assert os.path.exists(config_path), "Config file isn't found"
        
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            
        Config.set_field(MODEL_NAME_FIELD, config)
        Config.check_field(MODEL_ARGS_FIELD, config)
        Config.check_field(MODEL_TRAIN_ARGS_FIELD, config)
        Config.check_field(TARGET_FUNCTION_FIELD, config)
        Config.check_field(TARGET_FUNCTION_ARGS_FIELD, config)
        Config.check_field(DATA_PATH_FIELD, config)
        Config.check_field(TICKERS_FIELD, config)
        
        self.model_name = config[MODEL_NAME_FIELD]
        self.model_args = config[MODEL_ARGS_FIELD]
        
        
    def set_field(self, field: str, config: Dict):
        assert field in config, f"Field {field} is not in config"
        
        setattr(self, field, config[field])
    