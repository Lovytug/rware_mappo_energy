from pathlib import Path
from abc import ABC, abstractmethod

class ReaderFile(ABC):
    """
    Docstring для ReaderFile

    Базовый класс от которого создаются все считывающие классы файлы

    """
    
    def __init__(self, path_file: Path):
        self.path = path_file

    @abstractmethod
    def read(self):
        pass
