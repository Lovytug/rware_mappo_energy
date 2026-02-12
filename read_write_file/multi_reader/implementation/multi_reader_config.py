from read_write_file.multi_reader.base.multi_reader import MultiReader
from typing import Any

class MultiReaderConfigJSON(MultiReader):
    """
    Docstring для MultiReaderConfigJSON

    Реализация мульти считывателя для конфига типа json

    """

    def get(self) -> dict[str, Any]:
        result = {}
        for reader in self.readers:
            result.update(reader.get())

        return result