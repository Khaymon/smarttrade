import pandas as pd
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
                start = pd.Timestamp.min
            if stop is None:
                stop = pd.Timestamp.max
            
            if not isinstance(start, pd.Timestamp) or not isinstance(stop, pd.Timestamp):
                raise IndexError("Slice must contain only pandas Timestamps")

            mask = (self.data.index >= start) & (self.data.index < stop) 
            return self._construct(self.data[mask].copy())
    
    
    def _construct(self, data: pd.DataFrame):
        raise NotImplementedError
    
    
    def start_date(self) -> pd.Timestamp:
        return self.data.index.min()


    def end_date(self) -> pd.Timestamp:
        return self.data.index.max()


    def dates_range(self) -> Tuple[pd.Timestamp, pd.Timestamp]:
        return self.start_date(), self.end_date()
    
    
    def get_data(self) -> pd.DataFrame:
        return self.data.copy()
    
    
    def __len__(self) -> int:
        return len(self.data)