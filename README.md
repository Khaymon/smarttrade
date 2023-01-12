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

## Main entities

### Containers
Containers are classes wich contains some data in it.
#### Data Containers
Every type of market data should be placed in one of the __DataContainer__ inheritors.
- __StockData.__ This entity holds a data for a concrete stock. You can create this by passing 1) a `ticker` and 2) raw pandas DataFrame or path to a folder where file `ticker`.csv is located. Both DataFrame and file should contain columns with names `date`, `low`, `open`, `volume`, `high` and `close`.
- __StocksList.__ This entity contains the information about several stocks. It's needed when training a single model for different tickers.

#### Task Containers
`TaskContainer` class contains __DataContainer__ and __Target__.

### Feature engineering
When you need to preprocess your data in order to get more information from it you have to use __Feature__ class in one of its forms. This class expects its inheritors to override `compute` method which takes one of the data containers and returns a pandas Series with feature.
