from dataclasses import dataclass
import typing as T

from .base_container import BaseContainer


@dataclass
class ArticleContainer(BaseContainer):
    text: str
    header: T.Optional[str]
    link: T.Optional[str]
