from ..containers import StocksData, StocksTarget
import numpy as np
import pandas as pd
import torch
from typing import List, Any


class StocksDataModelPreprocessor:
    def preprocess(self, stocks_data: StocksData, target: StocksTarget, **kwargs) -> Any:
        raise NotImplementedError
    
    @staticmethod
    def split(stocks_data: StocksData, target: StocksTarget = None, left_ratio: float = 0.8, threshold: str = None):
        start_date, end_date = stocks_data.dates_range()
        
        if threshold is not None:
            threshold = pd.Timestamp(threshold)
        else:
            threshold = start_date + (end_date - start_date) * left_ratio
        
        if target is not None:
            return stocks_data[:threshold], stocks_data[threshold:], target[:threshold], target[threshold:]
        else:
            stocks_data[:threshold], stocks_data[threshold:]
        
        
class SimpleModelPreprocessor(StocksDataModelPreprocessor):
    def preprocess(self, stocks_data: StocksData, target: StocksTarget, dropna: bool = True, return_tensors: bool = True):
        stocks_data_df = stocks_data.get_data()
        target_df = target.get_data()
        
        full_data = pd.merge(stocks_data_df, target_df, on=["date", "ticker"])
        
        if dropna:
            full_data = full_data.dropna()
        else:
            full_data = full_data.dropna(subset=[target.target_name])
        
        X = full_data.drop(["ticker", target.target_name], axis=1).to_numpy()
        y = full_data[target.target_name].to_numpy()
        
        if return_tensors:
            X = torch.tensor(X)
            y = torch.tensor(y)
            
        return X, y


class SequenceModelPreprocessor(StocksDataModelPreprocessor):
    def __init__(self, sequence_lenght: int = 10):
        self.sequence_length = sequence_lenght
        
    
    def preprocess(self, stocks_data: StocksData, target: StocksTarget, return_tensors=True):
        simple_preprocessor = SimpleModelPreprocessor()
        X_sequences = []
        y_sequences = []
        
        for ticker in stocks_data.get_tickers():
            ticker_data = stocks_data.filter_ticker(ticker)
            X, y = simple_preprocessor.preprocess(ticker_data, target, return_tensors=return_tensors)
            
            for idx in range(0, len(X) - self.sequence_length):
                X_sequences.append(X[idx:idx + self.sequence_length])
                y_sequences.append(y[idx:idx + self.sequence_length])
                    
                
        return X_sequences, y_sequences