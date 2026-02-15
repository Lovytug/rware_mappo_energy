from abc import ABC, abstractmethod
from read_write_file.reader.base.reader_file import ReaderFile, ReadResult
from pathlib import Path
from util.path import CONFIG_EPISODE_RUN
from util.global_var import NAME_RUN_CONFIG_EVER_EPISODE
import json
import os


class ReaderConfigFileForRun(ReaderFile, ABC):

    def __init__(self):
        super().__init__("")
        self.path = os.path.join(CONFIG_EPISODE_RUN, NAME_RUN_CONFIG_EVER_EPISODE+".json")


    @abstractmethod
    def read(self) -> ReadResult:
        pass
    