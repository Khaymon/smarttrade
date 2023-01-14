# 💰 Trading algorithms
Hello there👋 It's a minimalistic repository with machine learning and deep learning algorithms for stock market trading. Please, see `examples` directory with code snippets.
## Installation
- Clone the repo and cd into it:
```bash
git clone https://github.com/Khaymon/trading-algorithms.git
cd trading-algorithms
```
- Install required packages:
```
pip install -r requirements.txt
```

## Downloading the data
### Stock market data
Data is loaded by `yahoo-finance` module. You can use `yf_download_data.py` for it.
```bash
python yf_download_data.py
```

## Entities
### Containers
Containers are classes, which collect some data in it. Main class for stocks market data is `StocksData`. `StocksTarget` class is used to save a target for a concrete task.

### Features
Features are some functions from market data. Important thing to understand before constructing your own `Feature` is that function shouldn't look forward in time. `FeaturesList` is used to aggregate many of `Features` in one place.


### Target functions
`TargetFunction` is a class, which defines a function creating a target data. It can be either regression or classification target.


### Model preprocessors
Model preprocessors takes stocks data and target to prepare it for being placed in a model.


### Models
Of course, there are a models, which take the input produced by specific model preprocessor and make predictions.

## Results
| # | Train stocks | Test stocks | Train period                              | Test period                               | Target              | Algorithm         | Metric      |
| ------------ | ----------------- | ---------------- | ----------------------------------------- | ----------------------------------------- | ------------------- | ----------------- | ----------- |
| 1            | AAPL              | AAPL             | 2021-01-25 14:30 - 2022-11-11 20:30 | 2022-11-14 14:30 - 2023-01-12 21:00 | Close Price +3 bars | CatBoostRegressor | 0.0127 MAPE |
| 2            | AAPL              | AAPL             | 2021-01-25 14:30 - 2022-11-11 20:30 | 2022-11-14 14:30 - 2023-01-12 21:00 | Close Price +3 bars | Current Close     | 0.0098 MAPE |
|              |                   |                  |                                           |                                           |                     |                   |             |
