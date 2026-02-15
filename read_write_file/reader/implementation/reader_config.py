from pathlib import Path
from read_write_file.reader.base.reader_file import ReaderFile, ReadResult
from read_write_file.reader.base.reader_file_run import ReaderConfigFileForRun
from abc import ABC
import json
import os


class ReaderConfigJSON(ReaderFile):
    """
    Docstring для ReaderConfig

    Класс для считывания конфиг файлов типа json

    """

    def read(self) -> ReadResult:
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return ReadResult(
            data=data,
            filename=Path(self.path).name,
            path=self.path
        )
    
class ReaderConfigJSONRun(ReaderConfigFileForRun):

    def __init__(self):
        super().__init__()

    def read(self) -> ReadResult:
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return ReadResult(
            data=data,
            filename=Path(self.path).name,
            path=self.path
        )