import pandas as pd
import numpy as np
from datetime import datetime
from typing import Tuple


class TimeDataContainer:
    def __init__(self):
        self.data = None
        
        
    def __getitem__(self, key):
        if not isinstance(key, slice):
            return self._construct(self.data[key].copy())
        else:
            if key.step is not None:
                raise IndexError("Slice step is not supported in time data")
            
            start = key.start
            stop = key.stop
            
            if start is None:
                start = self.start_date()
            if stop is None:
                stop = self.end_date()

            mask = (self.data.index >= start) & (self.data.index < stop) 
            return self._construct(self.data[mask].copy())
    
    
    def _construct(self, data: pd.DataFrame):
        raise NotImplementedError
    
    
    def start_date(self) -> pd.Timestamp:
        return self.data.reset_index().groupby("ticker")["date"].min().min()


    def end_date(self) -> pd.Timestamp:
        return self.data.reset_index().groupby("ticker")["date"].max().min()


    def dates_range(self) -> Tuple[pd.Timestamp, pd.Timestamp]:
        return self.start_date(), self.end_date()
    
    
    def get_data(self) -> pd.DataFrame:
        return self.data.copy()
    
    
    def __len__(self) -> int:
        return len(self.data)
    
    
    def __iter__(self):
        self.iterator = 0
        
        return self
    

    def __next__(self):
        if (self.iterator < len(self)):
            data = self.data.iloc[self.iterator].copy()
            self.iterator += 1
        else:
            raise StopIteration

        return data