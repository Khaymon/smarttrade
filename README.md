# 💰 Smart Trade
Hello there👋 It's a minimalistic repository with machine learning and deep learning algorithms for stock market trading. For examples and code snippets, please, see the `examples` directory.

## Table of contents
1. [Installation](#installation)
2. [Downloading the data](#downloading)
    1. [Stock market data](#downloading_stock_market_data)
    2. [News data](#downloading_news_data)
3. [Entities](#entities)
    1. [Containers](#containers)
    2. [Features](#features)
    3. [Target functions](#target_functions)
    4. [Model preprocessors](#model_preprocessors)
    5. [Models](#models)
4. [Results](#results)
5. [Todo](#todo)
## Installation <a name="installation"></a>
- Clone the repo and cd into it:
```bash
git clone https://github.com/Khaymon/trading-algorithms.git
cd trading-algorithms
```
- Install required packages:
```
pip install -r requirements.txt
```

## Downloading the data <a name="downloading"></a>
### Stock market data <a name="downloading_stock_market_data"></a>
Data is loaded by `yahoo-finance` module. You can use the `yf_download_data.py` file to get the TOP-100 US liquidity stocks market data.
```bash
python yf_download_data.py
```

### News data <a name="downloading_news_data"></a>
Scrapping is our everything. Data is collected by selenium package. You need to install ChromeDriver in order to scrape investingview.com website. In the file `investing_view_scrape.py` you can change URL in order to receive either political or finance news. In order to get news data, just call
```bash
python yf_download_data.py
```

## Entities <a name="entities"></a>
### Containers <a name="containers"></a>
Containers are classes, which collect some data in it. Main class for stocks market data is `StocksData`. `StocksTarget` class is used to save a target for a concrete task.

### Features <a name="features"></a>
Features are some functions from market data. Important thing to understand before constructing your own `Feature` is that function shouldn't look forward in time. `FeaturesList` is used to aggregate many of `Features` in one place.


### Target functions <a name="target_functions"></a>
`TargetFunction` is a class, which defines a function creating a target data. It can be either regression or classification target.


### Model preprocessors <a name="model_preprocessors"></a>
Model preprocessors takes stocks data and target to prepare it for being placed in a model.


### Models <a name="models"></a>
Of course, there are models, which take the input produced by specific model preprocessor and make predictions.

## Results <a name="results"></a>
Please, check results in results.md file.

## Todo <a name="todo"></a>

- [ ] Write backtesting class
- [ ] Experiment with only news headers embeddings
