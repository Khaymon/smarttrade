import os
import json
from typing import Dict

CONFIG_FIELDS = dict(
    MODEL_NAME_FIELD = "model_name",
    MODEL_ARGS_FIELD = "model_args",
    MODEL_TRAIN_ARGS_FIELD = "model_train_args",
    TARGET_FUNCTION_FIELD = "target_function",
    TARGET_FUNCTION_ARGS_FIELD = "target_function_args",
    DATA_PATH_FIELD = "data_path",
    TICKERS_FIELD = "tickers",
    METRIC_FIELD = "metric"
)


class Config:
    def __init__(self, config_path: str) -> None:
        assert os.path.exists(config_path), "Config file isn't found"
        
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            
        for _, key in CONFIG_FIELDS.items():
            self.set_field(key, config)
        
    def set_field(self, key: str, config: Dict):
        assert key in config, f"Field {key} is not in config"
        
        setattr(self, key, config[key])
    