from dataclasses import dataclass

from .base_container import BaseContainer


class CandleInterval:
    MINUTE = "m"
    HOUR = "h"
    DAY = "d"
    WEEK = "w"


@dataclass
class CandleContainer(BaseContainer):
    ticker: str
    interval: CandleInterval
    open: float
    close: float
    volume: float
    high: float
    low: float
