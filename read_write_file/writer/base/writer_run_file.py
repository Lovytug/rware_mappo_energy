import os

from abc import ABC, abstractmethod
from read_write_file.writer.base.writer_file import WriterFile

from util.path import PROJECT_ROOT
from util.global_var import NAME_RUN_CONFIG_EVER_EPISODE


class WriterFileForRun(WriterFile, ABC):

    def __init__(self):
        super().__init__("")

        run = "run"

        self.path = os.path.join(PROJECT_ROOT, run)

        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)
            print(f"Папка 'run' создана: {self.path}")
        else:
            pass

    @abstractmethod
    def save(self, data, name_save: str, overwrite=False):
        pass


class WriterConcreteFileNameForRunEpisode(WriterFileForRun, ABC):

    def __init__(self):
        super().__init__()

        self.path = os.path.join(self.path, NAME_RUN_CONFIG_EVER_EPISODE)

    @abstractmethod
    def save(self, data, append=False, overwrite=False):
        pass

