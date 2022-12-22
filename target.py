from stock_data import StockData
import pandas as pd


class Target:
    def calculate(self, stock_data: StockData) -> pd.Series:
        raise NotImplementedError
    
    
class ClosePriceTarget(Target):
    def __init__(self, bars_count: int) -> None:
        self.bars_count = bars_count
        
    def calculate(self, stock_data: StockData) -> pd.Series:
        target = stock_data.get_column("close").shift(-self.bars_count)
        target.name = f"close_target_{self.bars_count}_bars"
        
        return target