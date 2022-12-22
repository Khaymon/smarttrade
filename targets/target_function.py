from stock_data import StockData, StocksList
from .target import Target, TargetsList
from .task import Task

import pandas as pd
from typing import Any


class TargetFunction:
    def __init__(self) -> None:
        self.task = None
    
    def get(self, stock_data: StockData) -> Target:
        raise NotImplementedError
    
    def from_stocks_list(self, stocks_list: StocksList):
        targets_list = []
        for stock_data in stocks_list:
            targets_list.append(self.get(stock_data))
            
        return TargetsList(task=self.task, targets_list=targets_list)

    
class ClosePriceTargetFunction(TargetFunction):
    def __init__(self, bars_count: int) -> None:
        self.bars_count = bars_count
        self.task = Task.REGRESSION
        
    def get(self, stock_data: StockData) -> Target:
        target = stock_data.get("close").shift(-self.bars_count)
        target.name = f"close_target_{self.bars_count}_bars"
        
        return Target(ticker=stock_data.ticker, task=self.task, target=target)