from stock_data import StockData
import pandas as pd


class StockFeature:
    def compute(self, stock_data: StockData) -> pd.Series:
        raise NotImplementedError
    

class MovingAggregateFeature(StockFeature):
    def __init__(self, function_name: str, column: str, window: int) -> None:
        super().__init__()
        
        self.function_name = function_name
        self.column = column
        self.window = window
    
    def compute(self, stock_data: StockData) -> pd.Series:
        feature = stock_data.get_column(self.column).rolling(self.window).agg(self.function_name)
        feature.name = f"{self.column}_{self.window}_{self.function_name}"
        
        return feature


class DayFeature(StockFeature):
    def compute(self, stock_data: StockData) -> pd.Series:
        days = stock_data.get_dates().dt.day
        
        return days
        

class WeekdayFeature(StockFeature):
    def compute(self, stock_data: StockData) -> pd.Series:
        weekdays = stock_data.get_dates().dt.weekday
        
        return weekdays
    

class MonthFeature(StockFeature):
    def compute(self, stock_data: StockData) -> pd.Series:
        months = stock_data.get_dates().dt.month
        
        return months
        

