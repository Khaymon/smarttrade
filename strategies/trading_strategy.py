from data_tools.model_preprocessors import StocksDataModelPreprocessor
from features import FeaturesList
from models import StocksModel

import numpy as np
from dataclasses import dataclass
from backtesting import Strategy


@dataclass
class MarketOrder:
    direction: str
    size: float
    limit: float = None
    stop: float = None
    sl: float = None
    tp: float = None


class TradingStrategy(Strategy):
    def init(self, 
             features_list: FeaturesList,
             model_preprocessor: StocksDataModelPreprocessor,
             stock_model: StocksModel):
        
        self.features_list = features_list
        self.model_preprocessor = model_preprocessor
        self.stock_model = stock_model
    
    
    def next(self):
        current_data = self.data.df.copy()
        current_data = current_data.rename({
            "Close": "close",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Volume": "volume"
        }, axis=1)
        
        current_data = self.features_list.transform(current_data)
        X = self.model_preprocessor.preprocess(current_data)
        predictions = self.stock_model.predict(X)
        
        market_order = self.get_order(predictions[-1])
        self.make_order(market_order)
        
    
    def get_order(self, prediction) -> MarketOrder:
        raise NotImplementedError
    
    
    def make_order(self, order):
        if order.direction == "buy":
            return self.buy(size=order.size,
                     limit=order.limit,
                     stop=order.stop,
                     sl=order.sl,
                     tp=order.tp
            )
        elif order.direction == "sell":
            return self.sell(size=order.size,
                     limit=order.limit,
                     stop=order.stop,
                     sl=order.sl,
                     tp=order.tp
            )