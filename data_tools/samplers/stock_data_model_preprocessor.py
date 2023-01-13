from ..containers import StocksData, StocksTarget
import numpy as np
import pandas as pd
from typing import List, Any


class StocksDataModelPreprocessor:
    @staticmethod
    def preprocess(stocks_data: StocksData, target: StocksTarget) -> Any:
        raise NotImplementedError
    
    @staticmethod
    def split(stocks_data: StocksData, target: StocksTarget = None, left_ratio: float = 0.8):
        start_date, end_date = stocks_data.dates_range()
        
        threshold = start_date + (end_date - start_date) * left_ratio
        
        if target is not None:
            return stocks_data[:threshold], stocks_data[threshold:], target[:threshold], target[threshold:]
        else:
            stocks_data[:threshold], stocks_data[threshold:]
        
        
class SimpleModelPreprocessor(StocksDataModelPreprocessor):
    @staticmethod
    def preprocess(stocks_data: StocksData, target: StocksTarget):
        stocks_data_df = stocks_data.get_data()
        target_df = target.get_data()
        
        full_data = pd.merge(stocks_data_df, target_df, on=["date", "ticker"])
        full_data = full_data.dropna(subset=[target.target_name])
        
        X = full_data.drop(["ticker", target.target_name], axis=1)
        y = full_data[target.target_name]
            
        return X.to_numpy(), y.to_numpy()
