from abc import ABC, abstractmethod
from typing import Any

class DataExtracter(ABC):
    """
    Docstring для DataExtracter

    Данный класс предназначен для удобного извлечения соответствующих данных из файлов

    """
    @staticmethod
    @abstractmethod
    def extract(data) -> Any:
        pass
        

