from environments.base.builder.builder_conf import BuilderConfig, RuntimeContext

from read_write_file.reader.base.reader_file import ReaderFile
from read_write_file.writer.base.writer_run_file import WriterConcreteFileNameForRunEpisode

from environments.base.extract_field_config.json.register_extractors import RegisterExtractors
from environments.base.extract_field_config.json.field_extractor import ScalerExtractor, CoordListExtractor


class BuilderEpisodeJSON(BuilderConfig):
    
    def __init__(self, reader: ReaderFile, writer: WriterConcreteFileNameForRunEpisode):
        self.reader = reader
        self.writer = writer

        self.data, self.filename = reader.read().data, reader.read().filename
        self.filename = self.filename.replace('.json', '')

        self.register = RegisterExtractors()
        self.register.regist([ScalerExtractor(), CoordListExtractor()])


    def build(self, ctx: RuntimeContext):
        self.register.set_context(ctx)
        
        result = {}
        result[self.filename] = self._generate_recursive(self.data)
        self.writer.save(result, append=True)


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