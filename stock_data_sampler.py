from stock_data import StockData
from target import Target
import numpy as np
from typing import List


class StockDataSampler:
    def sample(self, stock_data: StockData, target: Target):
        raise NotImplementedError
    

class SimpleStockDataSampler(StockDataSampler):
    def sample(self, stock_data: StockData, target: Target):
        data = stock_data.get().to_numpy()
        target = target.get().to_numpy()
        
        return data, target
