from dataclasses import dataclass
import typing as T

from .base_container import BaseContainer


@dataclass
class CandleContainer(BaseContainer):
    open: float
    close: float
    volume: float
    high: float
    low: float
