from dataclasses import dataclass
import typing as T

from .base_container import BaseContainer


@dataclass
class TextContainer(BaseContainer):
    text: str
    header: T.Optional[str]
    link: T.Optional[str]
