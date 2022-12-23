from .stock_model import StockModel
from targets.task import Task
from stock_data.samplers import SimpleStockDataSampler

from catboost import CatBoostRegressor
import numpy as np


class GBMRegressionModel(StockModel):
    def __init__(self, **kwargs) -> None:
        self.model = CatBoostRegressor(**kwargs)
        self.task = Task.REGRESSION
        self.sampler = SimpleStockDataSampler()
        
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> None:
        self.model.fit(X, y, **kwargs)
        
    def predict(self, X: np.ndarray, **kwargs) -> np.ndarray:
        predictions = self.model.predict(X, **kwargs)
        
        return predictions
    