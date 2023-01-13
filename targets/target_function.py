from data_tools.containers import StocksData
from .task import Task

import pandas as pd
from typing import Any, Union


class TargetFunction:
    def __init__(self) -> None:
        self.task = None
        self.target_name = None
        
    def _compute(self, data: pd.DataFrame) -> Any:
        raise NotImplementedError
    
    def get(self, stocks_data: StocksData) -> pd.DataFrame:
        targets_list = []
        for ticker in stocks_data.get_tickers():
            ticker_data = stocks_data.filter_ticker(ticker).get_data()
            target = self._compute(ticker_data)
            target.name = self.target_name
            
            ticker_column = pd.Series(ticker, index=target.index, name="ticker")
            targets_list.append(pd.concat([target, ticker_column], axis=1))
            
        target = pd.concat(targets_list)
        
        return target
        
    
class ClosePriceTargetFunction(TargetFunction):
    def __init__(self, bars_count: int) -> None:
        self.bars_count = bars_count
        self.task = Task.REGRESSION
        self.target_name = f"close_target_{self.bars_count}_bars"
        
    def _compute(self, data: pd.DataFrame) -> pd.Series:
        return data["close"].shift(-self.bars_count)
        
    