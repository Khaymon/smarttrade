from .base_logger import BaseLogger


class SimpleLogger(BaseLogger):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def info(self, message: str) -> None:
        print(self._get_message("| INFO |\t" + message))

    def warn(self, message: str) -> None:
        print(self._get_message("| WARN |\t" + message))

    def error(self, message: str) -> None:
        print(self._get_message("| ERROR |\t" + message))
