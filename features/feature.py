from data_tools.containers import StocksData

import re
import numpy as np
import pandas as pd
from typing import Union
from sklearn.decomposition import PCA


class Feature:
    def fit(self, stocks_data: StocksData):
        raise NotImplementedError
    
    def transform(self, stocks_data: Union[StocksData, pd.DataFrame]) -> StocksData:
        targets_list = []
        if type(stocks_data) == StocksData:
            for ticker in stocks_data.get_tickers():
                ticker_data = stocks_data.filter_ticker(ticker).get_data()
                ticker_target = self._compute(ticker_data)
                
                ticker_column = pd.Series(ticker, index=ticker_target.index, name="ticker")
                ticker_target = pd.concat([ticker_target, ticker_column], axis=1)
                
                targets_list.append(ticker_target)
        else:
            for ticker in stocks_data["ticker"].unique():
                ticker_data = stocks_data[stocks_data["ticker"] == ticker].copy()
                ticker_target = self._compute(ticker_data)
                
                ticker_column = pd.Series(ticker, index=ticker_target.index, name="ticker")
                ticker_target = pd.concat([ticker_target, ticker_column], axis=1)
                
                targets_list.append(ticker_target)
        
        target_df = pd.concat(targets_list)
        if type(stocks_data) == StocksData:
            stocks_data.add_feature(target_df)
        else:
            stocks_data.merge(target_df, how="left", on=["date", "ticker"])
        
        return stocks_data
    
    
    def fit_transform(self, stocks_data: StocksData) -> pd.DataFrame:
        
        self.fit(stocks_data)
        return self.transform(stocks_data)
    
    
    def _compute(self, ticker_data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError
    

class MovingAggregateFeature(Feature):
    def __init__(self, function_name: str, column: str, window: int) -> None:
        super().__init__()
        
        self.function_name = function_name
        self.column = column
        self.window = window
    
    
    def _compute(self, ticker_data: pd.DataFrame) -> pd.Series:
        feature = ticker_data.get(self.column).rolling(self.window).agg(self.function_name)
        feature.name = f"{self.column}_{self.window}_{self.function_name}"
        
        return feature
    
    
class DiffFeature(Feature):
    def __init__(self, first_column: str, second_column: str) -> None:
        super().__init__()
        
        self.first_column = first_column
        self.second_column = second_column
    
    
    def _compute(self, ticker_data: pd.DataFrame) -> pd.Series:
        diff = ticker_data["first_column"] / ticker_data["second_column"]
        diff.name = f"{self.first_column}_{self.second_column}_diff"
        
        return diff


class RatioFeature(Feature):
    def __init__(self, first_column: str, second_column: str) -> None:
        super().__init__()
        
        self.first_column = first_column
        self.second_column = second_column
    
    
    def _compute(self, ticker_data: pd.DataFrame) -> pd.Series:
        diff = ticker_data["first_column"] - ticker_data["second_column"]
        diff.name = f"{self.first_column}_{self.second_column}_ratio"
        
        return diff


class DayFeature(Feature):
    def _compute(self, ticker_data: pd.DataFrame) -> pd.Series:
        days = ticker_data.get_dates().dt.day
        days.name = "day"
        
        return days
        

class WeekdayFeature(Feature):
    def _compute(self, ticker_data: pd.DataFrame) -> pd.Series:
        weekdays = ticker_data.get_dates().dt.weekday
        weekdays.name = "weekday"
        
        return weekdays
    

class MonthFeature(Feature):
    def _compute(self, ticker_data: pd.DataFrame) -> pd.Series:
        months = ticker_data.get_dates().dt.month
        months.name = "month"
        
        return months
        

class OpenCloseDiffFeature(Feature):
    def _compute(self, ticker_data: pd.DataFrame) -> pd.Series:
        diff = ticker_data["open"] - ticker_data["close"]
        diff.name = "open_close_diff"
        
        return diff
    

class HighLowDiffFeature(Feature):
    def _compute(self, ticker_data: pd.DataFrame) -> pd.Series:
        diff = ticker_data["high"] - ticker_data["low"]
        diff.name = "high_low_diff"
        
        return diff


class NewsFeature(Feature):
    def __init__(self, 
                 embeddings_path: str,
                 smooth_type: str = "exponential",
                 alpha: float = 0.9,
                 principal_components: int = 32):
        
        self.news_embeddings = pd.read_csv(embeddings_path, parse_dates=["date"], index_col="date")
        self.news_embeddings = self.news_embeddings.sort_index()
        self.smooth_type = smooth_type
        self.alpha = alpha
        
        self.principal_components = principal_components
        self.pca = PCA(n_components=principal_components)
        
        self.file_name = re.findall("([^/]+)\.csv", embeddings_path)[0]
    
    def fit(self, stocks_data: StocksData):
        train_data = self.news_embeddings[self.news_embeddings.index <= stocks_data.end_date()]
        self.pca.fit(train_data)
    
        
    def _compute(self, ticker_data: pd.DataFrame) -> pd.DataFrame:
        news_transformed = pd.DataFrame(self.pca.transform(self.news_embeddings), index=self.news_embeddings.index)
        news_ewm = news_transformed.ewm(alpha=self.alpha).mean()
        
        ticker_data = ticker_data.sort_index()
        
        embeddings = {}
        for idx in range(len(ticker_data)):
            ticker_row = ticker_data.iloc[idx]
            news_embedding = news_ewm[news_ewm.index <= ticker_row.name]
            if len(news_embedding) == 0:
                continue
            embeddings[ticker_row.name] = news_embedding.iloc[-1]
        
        result = pd.DataFrame(embeddings).T
        result.index.name = "date"
        result.columns = [f"{self.file_name}_emb_{i}" for i in range(self.principal_components)]
        
        return result
            
        