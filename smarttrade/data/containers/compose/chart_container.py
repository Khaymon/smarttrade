from dataclasses import dataclass
import typing as T

from smarttrade.data.containers.base import CandleContainer

from .compose_container import ComposeContainer


@dataclass
class TickerChartContainer(ComposeContainer):
    def __init__(self, candles: T.List[CandleContainer] = None) -> None:
        if candles:
            dates = set(map(lambda candle: candle.date, candles))
            if len(dates) != len(candles):
                raise ValueError(f"Found multiple dates for different candles")

        if any([candle.interval != candles[0].interval for candle in candles]):
            raise ValueError(f"Candles intervals are not equal")
        
        if any([candle.ticker != candles[0].ticker for candle in candles]):
            raise ValueError(f"Candles have different tickers")
        
        super().__init__(candles)
