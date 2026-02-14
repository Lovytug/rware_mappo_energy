from environments.base.builder.builder_conf import BuilderConfig

from read_write_file.reader.base.reader_file import ReaderFile
from read_write_file.writer.base.writer_file import WriterFile

from extract_field_config.json.register_extractors import RegisterExtractors
from extract_field_config.json.field_extractor import ScalerExtractor, CoordListExtractor


class BuilderEpisodeJSON(BuilderConfig):
    
    def __init__(self, reader: ReaderFile, writer: WriterFile):
        self.reader = reader
        self.writer = writer
        self.data = reader.read().copy()

        self.register = RegisterExtractors()
        self.register.regist([ScalerExtractor(), CoordListExtractor()])


    def build(self):
        result = self._generate_recursive(self.data)
        self.writer.save(result, NAME_RUNS_CONFIG, overwrite=True)


    def _generate_recursive(self, cfg: dict) -> dict:
        result = {}

        for field_name, field in cfg.items():
            if field_name == 'type':
                continue

            if isinstance(field, dict) and 'type' in field:
                result[field_name] = self.register.resolve(name=field_name, cfg=field)

            elif isinstance(field, dict) and 'type' not in field:
                result[field_name] = self._generate_recursive(field)

            else:
                result[field_name] = field

        return result