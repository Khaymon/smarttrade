class StockModel:
    def __init__(self):
        self.task = None
    
    def fit(self, *args, **kwargs) -> None:
        raise NotImplementedError
    
    def predict(self, *args, **kwargs):
        raise NotImplementedError