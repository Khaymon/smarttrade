from dataclasses import dataclass
import datetime


@dataclass
class BaseContainer:
    date: datetime.datetime
