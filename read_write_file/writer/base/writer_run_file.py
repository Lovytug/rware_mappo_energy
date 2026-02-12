import os
from abc import ABC, abstractmethod
from read_write_file.writer.base.writer_file import WriterFile
from util.path import PROJECT_ROOT


class WriterFileForRun(WriterFile):

    def __init__(self):
        super().__init__()

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