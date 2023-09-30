class BaseLogger:
    def __init__(self, name: str) -> None:
        self._name = name

    def _get_message(self, message: str) -> str:
        return f"#\t[{self._name}]\t{message}"

    def info(self, message: str) -> None:
        raise NotImplementedError()
    
    def warn(self, message: str) -> None:
        raise NotImplementedError()
    
    def error(self, message: str) -> None:
        raise NotImplementedError()
