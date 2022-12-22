import yfinance as yf
import pandas as pd
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


def main():
    from_date = pd.Timestamp.now() - pd.Timedelta(days=720)
    to_date = pd.Timestamp.now()
    
    data = yf.download(STOCKS_TICKERS, start=from_date, end=to_date, interval="1h")
    data = pd.DataFrame(data).swaplevel(axis=1)
    data.index.name = "Date"

    for ticker in STOCKS_TICKERS:
        ticker_data = data[ticker]
        
        file_name = os.path.join(DATA_PATH, ticker + ".csv")
        ticker_data.to_csv(file_name)


if __name__ == "__main__":
    main()