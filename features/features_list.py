from .feature import *
from typing import List


class FeaturesList:
    def __init__(self, features: List[Feature] = None) -> None:
        if features is None:
            self.features = []
        else:
            self.features = features
        
    def append(self, feature: Feature) -> None:
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


    def preprocess(self, stocks_data: StocksData) -> StocksData:
        for feature in self:
            stocks_data.add_feature(feature.get(stocks_data))
        
        return stocks_data
        

class IndicatorsFeaturesList(FeaturesList):
    def __init__(self) -> None:
        super().__init__()
        
        close_moving_averages = [
            MovingAggregateFeature(function_name="mean", column="close", window=5),
            MovingAggregateFeature(function_name="mean", column="close", window=10),
            MovingAggregateFeature(function_name="mean", column="close", window=20)
        ]
        
        close_moving_variances = [
            MovingAggregateFeature(function_name="var", column="close", window=5),
            MovingAggregateFeature(function_name="var", column="close", window=10),
            MovingAggregateFeature(function_name="var", column="close", window=20)
        ]
        
        self.expand(close_moving_averages)
        self.expand(close_moving_variances)
        
        