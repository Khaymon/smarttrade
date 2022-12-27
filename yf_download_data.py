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

DATA_PATH = "./data/"


def download_data(tickers: List[str], from_date: pd.Timestamp, to_date: pd.Timestamp) -> pd.DataFrame:
    data = yf.download(tickers, start=from_date, end=to_date, interval="1h")
    data = pd.DataFrame(data).swaplevel(axis=1)
    data.index.name = "Date"
    data.index = data.index.tz_convert(None)
        
    return data


def save_data(data: pd.DataFrame, data_path: str) -> None:
    tickers = data.columns.get_level_values(0)
    
    for ticker in tickers:
        ticker_data = data[ticker]
        
        file_name = os.path.join(data_path, ticker + ".csv")
        ticker_data.to_csv(file_name)


def main():
    from_date = pd.Timestamp.now() - pd.Timedelta(days=720)
    to_date = pd.Timestamp.now()
    
    data = download_data(STOCKS_TICKERS, from_date, to_date)
    save_data(data, DATA_PATH)


if __name__ == "__main__":
    main()