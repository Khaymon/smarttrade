import argparse
import yfinance as yf
import pandas as pd
from typing import List
import os

STOCKS_TICKERS = [
    "AAPL", "MSFT", "GOOG", "AMZN", "BRK-B", "UNH", "JNJ", "XOM", "V", "TSLA", "NVDA", "WMT", "JPM",
    "PG", "LLY", "CVX", "MA", "HD", "META", "PFE", "ABBV", "MRK", "KO", "BAC", "PEP", "AVGO", "ORCL",
    "TMO", "COST", "MCD", "CSCO", "DHR", "ABT", "NKE", "TMUS", "NEE", "VZ", "ADBE", "DIS", "BMY",
    "PM", "WFC", "UPS", "CMCSA", "SCHW", "TXN", "RTX", "MS", "COP", "HON", "AMGN", "NFLX", "DE",
    "CRM", "T", "UNP", "LMT", "IBM", "QCOM", "CAT", "ELV", "CVS", "LOW", "GS", "BA", "SBUX", "SPGI",
    "INTU", "AXP", "INTC", "GILD", "BLK", "AMD", "PLD", "CI", "ADP", "AMT", "ISRG", "MDLZ", "SYK",
    "TJX", "GE", "C", "EL", "AMAT", "ADI", "NOC", "MMC", "MO", "REGN", "MRNA", "DUK", "NOW", "PYPL",
    "SO", "EOG", "BKNG", "PGR", "SLB", "VRTX"
]
DATA_PATH = "./data/market_data/"
RENAME_DICT = {
    "Date": "date",
    "High": "high",
    "Low": "low",
    "Open": "open",
    "Close": "close",
    "Volume": "volume"
}
KEEP_COLUMNS = ["high", "low", "open", "close", "volume"]


def download_data(tickers: List[str], from_date: pd.Timestamp, to_date: pd.Timestamp,
                  time_interval: str = "1h") -> pd.DataFrame:
    data = yf.download(tickers, start=from_date, end=to_date, interval=time_interval)
    
    data = data.rename(RENAME_DICT, axis=1, level=0)
    data = data[KEEP_COLUMNS]
    data = pd.DataFrame(data).swaplevel(axis=1)
    
    data.index.name = "date"
    
    return data


def save_data(data: pd.DataFrame, data_path: str) -> None:
    tickers = data.columns.get_level_values(0)
    
    for ticker in tickers:
        ticker_data = data[ticker].copy()
        ticker_data["ticker"] = ticker
        
        file_name = os.path.join(data_path, ticker + ".parquet")
        ticker_data.to_parquet(file_name)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="Market data downloader",
        description="Tool for downloading the market data for TOP-100 liquidity stocks"
    )
    
    parser.add_argument("-d", "--output-dir", type=str, dest="output_dir",
                        help="Output directory for downloaded data", required=True)
    parser.add_argument("-t", "--tikers", type=str, nargs="+", default="all", choices=STOCKS_TICKERS,
                        dest="tickers", help="Tickers to download")
    parser.add_argument("-i", "--interval", type=str, default="1h", dest="time_interval",
                        help="Time interval for stock market bars")
    
    return parser.parse_args()


def main():
    arguments = parse_arguments()
    print(arguments)
    if arguments.tickers == "all":
        arguments.tickers = STOCKS_TICKERS
    
    from_date = pd.Timestamp.now() - pd.Timedelta(days=720)
    to_date = pd.Timestamp.now()
    
    data = download_data(tickers=arguments.tickers, from_date=from_date, to_date=to_date,
                         time_interval=arguments.time_interval)
    save_data(data, arguments.output_dir)


if __name__ == "__main__":
    main()