from stock_data import StockData

import pandas as pd
from enum import IntEnum
from typing import Any


class Task(IntEnum):
    REGRESSION = 0
    CLASSIFICATION = 1


class Target:
    def __init__(self, task: Task = None, target: pd.Series = None) -> None:
        self.task = task
        self.target = target
    
    def _calculate(self, stock_data: StockData) -> pd.Series:
        raise NotImplementedError
    
    def get(self) -> pd.Series:
        assert self.target is not None, "Target is not computed!"
        
        return self.target.copy()
    
    def __len__(self):
        assert self.target is not None, "Target is not computed!"
        
        return len(self.target)
    
    def __getitem__(self, key: Any):
        assert self.target is not None, "Target is not computed!"
        target = self.get()
        
        if isinstance(key, slice):
            start = key.start
            stop = key.stop
            step = key.step
            
            if step is not None:
                raise IndexError("Step is not supported in slices!")
            
            if start is not None:
                if not isinstance(start, pd.Timestamp):
                    raise IndexError("Start of slice must be a Pandas Timestamp")
            else:
                start = pd.Timestamp.min
            
            if stop is not None:
                if not isinstance(stop, pd.Timestamp):
                    raise IndexError("Stop of slice must be a Pandas Timestamp")
            else:
                stop = pd.Timestamp.max
            
            mask = (target.index >= start) & (target.index < stop)
            return Target(task=self.task, target=target[mask])
        elif isinstance(key, int):
            return Target(task=self.task, target=target[mask])
        elif isinstance(key, pd.Timestamp):
            return Target(task=self.task, target=target[mask])
        else:
            raise IndexError("Index must be an integer, slice or Pandas Timestamp")

    
class ClosePriceTarget(Target):
    def __init__(self, stock_data: StockData, bars_count: int) -> None:
        self.bars_count = bars_count
        self.task = Task.REGRESSION
        
        self.target = self._calculate(stock_data)
        
    def _calculate(self, stock_data: StockData) -> pd.Series:
        target = stock_data.get("close").shift(-self.bars_count)
        target.name = f"close_target_{self.bars_count}_bars"
        
        return target