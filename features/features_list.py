from .feature import *

from typing import List
from itertools import product


class FeaturesList(Feature):
    def __init__(self, features: List[Feature] = None) -> None:
        if features is None:
            self.features = []
        else:
            self.features = features
        
    def append_feature(self, feature: Feature) -> None:
        self.features.append(feature)
        
    def expand(self, features: List[Feature]) -> None:
        self.features += features
        
    def __iter__(self):
        self.iterator = 0
        return self
    
    def __next__(self) -> Feature:
        assert self.features is not None, "Features are not set!"
        
        if self.iterator < len(self.features):
            feature = self.features[self.iterator]
            self.iterator += 1
            return feature
        else:
            raise StopIteration


    def fit(self, stocks_data: StocksData) -> None:
        for feature in self.features:
            feature.fit(stocks_data)
            
    
    def transform(self, stocks_data: StocksData) -> StocksData:
        for feature in self.features:
            feature.transform(stocks_data)
            
        return stocks_data
        

class IndicatorsFeaturesList(FeaturesList):
    def __init__(self) -> None:
        super().__init__()
        
        functions = ["mean", "max", "min", "median", "var"]
        columns = ["close", "open", "high", "low", "volume"]
        windows = [5, 10, 20]
        
        moving_aggregates = []
        for function, column, window in product(functions, columns, windows):
            feature = MovingAggregateFeature(function_name=function, column=column, window=window)
            moving_aggregates.append(feature)
            
        self.expand(moving_aggregates)
        