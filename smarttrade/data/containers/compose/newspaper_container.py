import typing as T

from smarttrade.data.containers.base import ArticleContainer

from .compose_container import ComposeContainer


class NewspaperContainer(ComposeContainer):
    def __init__(self, articles: T.Optional[T.List[ArticleContainer]] = None) -> None:
        super().__init__(articles)
