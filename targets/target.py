from .task import Task

import pandas as pd
from typing import List, Any


class Target:
    def __init__(self, ticker: str, task: Task, target: pd.Series) -> None:
        self.ticker = ticker
        self.task = task
        self.target = target

    def get(self) -> pd.Series:
        assert self.target is not None, "Target is not computed!"
        
        return self.target.copy()
    
    def __len__(self):
        assert self.target is not None, "Target is not computed!"
        
        return len(self.target)
    
    def get_dates(self):
        return pd.Series(self.target.index, name="date")
    
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
            return Target(ticker=self.ticker, task=self.task, target=target[mask])
        elif isinstance(key, int):
            return Target(ticker=self.ticker, task=self.task, target=target[mask])
        elif isinstance(key, pd.Timestamp):
            return Target(ticker=self.ticker, task=self.task, target=target[mask])
        else:
            raise IndexError("Index must be an integer, slice or Pandas Timestamp")
        

class TargetsList:
    def __init__(self, task: Task, targets_list: List[Target]) -> None:
        self.task = task
        self.targets_list = targets_list
        
    def __len__(self):
        return len(self.targets_list)
    
    def __getitem__(self, key):
        targets_list = []
        
        for target in self.targets_list:
            targets_list.append(target[key])
            
        return TargetsList(task=self.task, targets_list=targets_list)
    
    def get_target(self, index):
        return self.targets_list[index]
    
    def __iter__(self):
        self.iterator = 0
        
        return self
    
    def __next__(self):
        if self.iterator < len(self):
            target = self.get_target(self.iterator)
            self.iterator += 1
            
            return target
        else:
            raise StopIteration
    