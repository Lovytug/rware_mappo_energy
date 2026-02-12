from typing import Any
from read_write_file.reader.base.reader_file import ReaderFile
import json

class ReaderConfigJSON(ReaderFile):
    """
    Docstring для ReaderConfig

    Класс для считывания конфиг файлов типа json

    """

    def read(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)