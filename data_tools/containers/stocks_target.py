from .time_data_container import TimeDataContainer
from .stocks_data import StocksData
from targets import Task, TargetFunction

import pandas as pd
from typing import List, Any


class StocksTarget(TimeDataContainer):
    def __init__(self, task: Task, target: pd.DataFrame, target_name: str) -> None:
        self.task = task
        self.data = target
        self.target_name = target_name
        
    
    def _construct(self, target: pd.DataFrame):
        return StocksTarget(task=self.task, target=target, target_name=self.target_name)
    
    
    @staticmethod
    def from_target_function(stocks_data: StocksData, target_function: TargetFunction):
        target = target_function.get(stocks_data)
        
        return StocksTarget(task=target_function.task, target=target, target_name=target_function.target_name)