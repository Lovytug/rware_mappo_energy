from typing import Any
from abc import ABC, abstractmethod
from read_write_file.reader.base.reader_file import ReaderFile

class MultiReader(ABC):
    """
    Docstring для MultiReader

    Базовый класс для мульти считывателя, что собирает всю информацию со дургих считывателей

    """

    def __init__(self):
        self.readers: list[ReaderFile] = []

    def add(self, reader: ReaderFile):
        self.readers.append(reader)

    def add(self, readers: list[ReaderFile]):
        self.readers.extend(readers)

    @abstractmethod
    def get(self) -> dict[str, Any]:
        pass