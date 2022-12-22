from ..stocks_data_task import StocksDataTask
import numpy as np
from typing import List


class StockDataSampler:
    def sample(self, stock_data_task: StocksDataTask):
        raise NotImplementedError
    

class SimpleStockDataSampler(StockDataSampler):
    def sample(self, stock_data_task: StocksDataTask):
        stock_data_list = []
        target_data_list = []
        for stock_data, target in stock_data_task:
            stock_np = stock_data.get().to_numpy()
            target_np = target.get().to_numpy()
            
            mask = ~np.isnan(target_np)
            stock_np = stock_np[mask]
            target_np = target_np[mask]
            
            stock_data_list.append(stock_np)
            target_data_list.append(target_np)
            
        return np.vstack(stock_data_list), np.concatenate(target_data_list)
