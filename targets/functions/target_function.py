from stock_data import StockData, StocksList
from ..target import Target, TargetsList
from ..task import Task

import pandas as pd
from typing import Any, Union


class TargetFunction:
    def __init__(self) -> None:
        self.task = None
        
    def __call__(self, stocks_list: Union[StockData, StocksList]):
        if isinstance(stocks_list, StockData):
            self.get(stocks_list)
        elif isinstance(stocks_list, StocksList):
            targets_list = []
            for stock_data in stocks_list:
                targets_list.append(self.get(stock_data))
                
            return TargetsList(task=self.task, targets_list=targets_list)
        else:
            raise ValueError("Argument of call must be StockData or StocksList!")
    
    def get(self, stock_data: StockData) -> Target:
        raise NotImplementedError
        
    
class ClosePriceTargetFunction(TargetFunction):
    def __init__(self, bars_count: int) -> None:
        self.bars_count = bars_count
        self.task = Task.REGRESSION
        
    def get(self, stock_data: StockData) -> Target:
        target = stock_data.get("close").shift(-self.bars_count)
        target.name = f"close_target_{self.bars_count}_bars"
        
        return Target(ticker=stock_data.ticker, task=self.task, target=target)