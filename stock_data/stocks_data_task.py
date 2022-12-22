from stock_data import StocksList
from targets import TargetsList

import numpy as np
from typing import Tuple


class StocksDataTask:
    def __init__(self, stocks_list: StocksList, targets_list: TargetsList):
        StocksDataTask.check_sizes(stocks_list, targets_list)
        
        self.stocks_list = stocks_list
        self.targets_list = targets_list
        
    def __len__(self):
        return len(self.stocks_list)
    
    def __getitem__(self, key):
        stocks_list = self.stocks_list[key]
        targets_list = self.targets_list[key]
        
        return StocksDataTask(stocks_list=stocks_list, targets_list=targets_list)
    
    def from_date(self):
        return self.stocks_list.from_date()
    
    def to_date(self):
        return self.stocks_list.to_date()
    
    def dates_range(self):
        return self.from_date(), self.to_date()
    
    def split(self, left_side_ratio: float):
        from_date, to_date = self.dates_range()
        
        border_date = from_date + (to_date - from_date) * left_side_ratio
        
        return self[:border_date], self[border_date:]
    
    def __iter__(self):
        self.iterator = 0
        
        return self
    
    def __next__(self):
        if self.iterator < len(self):
            stock_data = self.stocks_list.get_stock_data(self.iterator)
            target = self.targets_list.get_target(self.iterator)
            
            self.iterator += 1
            return stock_data, target
        else:
            raise StopIteration
    
    @staticmethod
    def check_sizes(stocks_list: StocksList, targets_list: TargetsList):
        assert len(stocks_list) == len(targets_list), "Number of stocks and targets are not equal!"
        
        for stock_data, target in zip(stocks_list, targets_list):
            assert len(stock_data) == len(target), "Lengths of stock data and target are not equal!"
            assert np.all(stock_data.get_dates() == target.get_dates()), "Dates of stock data and target are not equal!"