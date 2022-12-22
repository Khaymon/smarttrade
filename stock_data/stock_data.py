import os
import pandas as pd
import numpy as np
from typing import List, Tuple, Any


class StockData:
    _keep_columns = ["Date", "Low", "Open", "Volume", "High", "Close"]
    _renaming_dict = {
        "Date": "date",
        "Low": "low",
        "Open": "open",
        "Volume": "volume",
        "High": "high",
        "Close": "close"
    }
    
    def __init__(self, ticker: str, data: pd.DataFrame = None, data_path: str = None):
        if data is not None:
            assert data.index.name == "date", "Date must be an index of data!"
            
            self.data = data.sort_index()
        elif data_path is not None:
            if not os.path.exists(data_path):
                raise FileNotFoundError(f"File {data_path} isn't found")
            
            data = pd.read_csv(data_path, parse_dates=["Date"])
            self.ticker = ticker
            
            # Keeping only columns needed
            data = data[self._keep_columns]
            
            # Renaming columns according to the renaming dict
            data = data.rename(self._renaming_dict, axis=1)
            
            data["date"] = data["date"].apply(lambda timestamp: pd.Timestamp(timestamp).tz_convert(None))
            
            self.data = data.set_index("date")
            self.data = self.data.dropna()
            self.data = self.data.sort_index()
        else:
            raise ValueError("data or data path should be provided!")
        
    def add_feature(self, feature: pd.Series):
        assert np.all(feature.index == self.data.index), "Feature indices must match data indices!"
        assert feature.name not in self.data.columns, "Feature should not be presented in data!"
        
        self.data[feature.name] = feature
        
    def features_count(self):
        return len(self.data.columns)
    
    def get(self, key: Any = None) -> pd.Series:
        data = self.data.copy()
        if key is None:
            return data
        else:
            return data[key].copy()
        
    def get_dates(self) -> pd.Series:
        return pd.Series(self.data.index, name="date")
    
    def from_date(self):
        return self.data.index.min()
    
    def to_date(self):
        return self.data.index.max()
    
    def dates_range(self):
        return self.from_date(), self.to_date()
        
    def __len__(self):
        assert self.data is not None, "Data is not set!"
        
        return len(self.data)
    
    def __getitem__(self, key: Any):
        assert self.data is not None, "Data is not set!"
        data = self.data.copy()
        
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
            
            mask = (data.index >= start) & (data.index < stop)
            return StockData(ticker=self.ticker, data=data[mask])
        elif isinstance(key, int):
            return StockData(ticker=self.ticker, data=data.iloc[key])
        elif isinstance(key, pd.Timestamp):
            return StockData(ticker=self.ticker, data=data.loc[key])
        else:
            raise IndexError("Index must be an integer, slice or Pandas Timestamp")
        
        
class StocksList:
    def __init__(self, stocks_list: List[StockData]) -> None:
        self.stocks_list = stocks_list
        
    def from_date(self) -> pd.Timestamp:
        min_date = self.stocks_list[0].from_date()
        
        for idx in range(1, len(self.stocks_list)):
            min_date = min(min_date, self.stocks_list[idx].from_date())
            
        return min_date
    
    def to_date(self) -> pd.Timestamp:
        max_date = self.stocks_list[0].to_date()
        
        for idx in range(1, len(self.stocks_list)):
            max_date = max(max_date, self.stocks_list[idx].to_date())
            
        return max_date
    
    def dates_range(self) -> Tuple[pd.Timestamp, pd.Timestamp]:
        return self.from_date(), self.to_date()
    
    def __len__(self):
        return len(self.stocks_list)
    
    def __getitem__(self, key: Any):
        stocks_list = []
        for stock_data in self.stocks_list:
            stocks_list.append(stock_data[key])
        
        return StocksList(stocks_list=stocks_list)
    
    def get_stock_data(self, index: int) -> StockData:
        return self.stocks_list[index]
    
    def __iter__(self):
        self.iterator = 0
        
        return self
    
    def __next__(self):
        if self.iterator < len(self):
            stock_data = self.get_stock_data(self.iterator)
            self.iterator += 1
            
            return stock_data
        else:
            raise StopIteration
    

class StockDataSplitter:
    @staticmethod
    def split(stocks_list: StocksList, left_ratio: float) -> Tuple[StockData, StockData]:
        from_date, to_date = stocks_list.dates_range()
        border = from_date + (to_date - from_date) * left_ratio
        
        left_stocks_list = stocks_list[:border]
        right_stocks_list = stocks_list[border:]
        
        return left_stocks_list, right_stocks_list