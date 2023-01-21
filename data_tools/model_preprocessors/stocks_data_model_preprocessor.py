from ..containers import StocksData, StocksTarget
import numpy as np
import pandas as pd
from datetime import datetime
import torch
from typing import List, Any, Union


class StocksDataModelPreprocessor:
    def preprocess(self, 
                   stocks_data: Union[StocksData, pd.DataFrame], 
                   target: Union[StocksTarget, pd.DataFrame] = None,
                   **kwargs) -> Any:
        raise NotImplementedError
    
    @staticmethod
    def split(stocks_data: StocksData, target: StocksTarget = None, left_ratio: float = 0.8, threshold: str = None):
        start_date, end_date = stocks_data.dates_range()
        
        if threshold is not None:
            threshold = pd.Timestamp(threshold).to_datetime64()
        else:
            threshold = start_date + (end_date - start_date) * left_ratio
        
        if target is not None:
            return stocks_data[:threshold], stocks_data[threshold:], target[:threshold], target[threshold:]
        else:
            stocks_data[:threshold], stocks_data[threshold:]
        
        
class SimpleModelPreprocessor(StocksDataModelPreprocessor):
    def preprocess(self, 
                   stocks_data: Union[StocksData, pd.DataFrame], 
                   target: Union[StocksTarget, pd.DataFrame] = None,
                   dropna: bool = True, 
                   return_tensors: bool = True):
        
        if type(stocks_data) == StocksData:
            stocks_data_df = stocks_data.get_data()
        else:
            stocks_data_df = stocks_data.get_data()
            
        if target is not None:
            if type(target) == StocksTarget:
                target_df = target.get_data()
            else:
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
        else:
            stocks_data_df = stocks_data_df.dropna()
            X = stocks_data_df.drop(["ticker"], axis=1).to_numpy()
            
            if return_tensors:
                X = torch.tensor(X)
            
            return X


class SequenceModelPreprocessor(StocksDataModelPreprocessor):
    def __init__(self, sequence_lenght: int = 10):
        self.sequence_length = sequence_lenght
        
    
    def preprocess(self, 
                   stocks_data: Union[StocksData, pd.DataFrame], 
                   target: Union[StocksTarget, pd.DataFrame] = None,
                   return_tensors=True):
        simple_preprocessor = SimpleModelPreprocessor()
        X_sequences = []
        y_sequences = []
        
        for ticker in stocks_data.get_tickers():
            ticker_data = stocks_data.filter_ticker(ticker)
            if target is not None:
                X, y = simple_preprocessor.preprocess(ticker_data, target, return_tensors=return_tensors)
            else:
                X = simple_preprocessor.preprocess(ticker_data, target, return_tensors=return_tensors)
            
            for idx in range(0, len(X) - self.sequence_length):
                X_sequences.append(X[idx:idx + self.sequence_length])
                if target is not None:
                    y_sequences.append(y[idx:idx + self.sequence_length])
                    
        if target is not None:
            return X_sequences, y_sequences
        else:
            return X_sequences
