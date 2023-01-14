from data_tools.containers import StocksData
import pandas as pd


class Feature:
    def get(self, stock_data: StocksData) -> pd.DataFrame:
        targets_list = []
        for ticker in stock_data.get_tickers():
            ticker_data = stock_data.filter_ticker(ticker).get_data()
            ticker_target = self._compute(ticker_data)
            
            ticker_column = pd.Series(ticker, index=ticker_target.index, name="ticker")
            ticker_target = pd.concat([ticker_target, ticker_column], axis=1)
            
            targets_list.append(ticker_target)
        
        return pd.concat(targets_list)
    
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
