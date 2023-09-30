from collections import defaultdict
from dataclasses import dataclass
import typing as T

from smarttrade.data.containers.base import BaseContainer


@dataclass
class ComposeContainer:
    def __init__(self, data: T.Optional[T.List[BaseContainer]] = None) -> None:
        self._data = defaultdict(list)
        
        for point in data:
            self._data[point.date].append(point)
