from .trading_strategy import TradingStrategy, MarketOrder

from data_tools.model_preprocessors import StocksDataModelPreprocessor
from features import FeaturesList
from models import StocksModel


class ClosePriceTargetStrategy(TradingStrategy):
    def init(self, 
             features_list: FeaturesList,
             model_preprocessor: StocksDataModelPreprocessor,
             stock_model: StocksModel,
             ratio: float = 0.01):
        
        super().init(features_list, model_preprocessor, stock_model)
        self.ratio = ratio
    
    def get_order(self, prediction):
        if ((prediction - self.data.Close) / self.data.Close >= self.ratio):
            return MarketOrder("buy", size=1)
        elif((prediction - self.data.Close) / self.data.Close <= -self.ratio):
            return MarketOrder("sell", size=1)