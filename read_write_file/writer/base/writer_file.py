from pathlib import Path
from abc import ABC, abstractmethod

class WriterFile(ABC):

    def __init__(self, path_file: Path):
        self.path = path_file

    @abstractmethod
    def save(self, data, name_save: str, overwrite=False):
        pass