from pathlib import Path
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class ReadResult:
    data: dict
    filename: str
    path: str

class ReaderFile(ABC):
    """
    Docstring для ReaderFile

    Базовый класс от которого создаются все считывающие классы файлы

    """
    
    def __init__(self, path_file: Path):
        self.path = path_file

    @abstractmethod
    def read(self) -> ReadResult:
        pass
