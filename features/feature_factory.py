from stock_data import StockData
from .features_list import FeaturesList


class FeatureFactory:
    @staticmethod
    def preprocess(stock_data: StockData, feature_list: FeaturesList) -> StockData:
        for feature in feature_list:
            stock_data.add_feature(feature.compute(stock_data))
        
        return stock_data