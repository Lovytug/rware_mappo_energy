from rware.warehouse import Warehouse

from generate_envs.generate_field.registry import GeneratorRegisrty
from generate_envs.generate_field.field_generator import ScalerGenerator, CoordListGenerator

from param_adapter.warehouse_adapter import WarehouseParamsAdapter

from generate_envs.generate_layers.generate_layers import GenerateLayers

from util.config_file import ReadConfigFileSystem, WriteConfigFileSystem
from util.path import CONFIG_EPISODE_RUN, CONFIGURATION_DIR
from util.global_var import NAME_RUNS_CONFIG, NAME_ORIGIN_CONFIG


class BuilderGenerateEnv:

    def __init__(self):
        self.reader = ReadConfigFileSystem(CONFIG_EPISODE_RUN)

    def build(self):
        data = self.reader.get(NAME_RUNS_CONFIG)

        geneartor_layout = GenerateLayers(data)
        adapter = WarehouseParamsAdapter(data)
        
        params = adapter.extract()

        return Warehouse(
            shelf_columns=params.shelf_columns,
            column_height=params.column_height,
            shelf_rows=params.shelf_rows,

            n_agents=params.n_agents,
            msg_bits=params.msg_bits,
            sensor_range=params.sensor_range,

            request_queue_size=params.request_queue_size,
            max_inactivity_steps=params.max_inactivity_steps,
            max_steps=params.max_steps,
            reward_type=params.reward_type,

            layout=geneartor_layout.generate()
        )
    

class BuilderConfigEpisode:

    def __init__(self):
        self.ctx = RuntimeContext()

        self.writer = WriteConfigFileSystem(CONFIG_EPISODE_RUN)

        reader = ReadConfigFileSystem(CONFIGURATION_DIR)
        self.base_conf = reader.get(NAME_ORIGIN_CONFIG)

        self.register = GeneratorRegisrty()
        self.register.regist(ScalerGenerator())
        self.register.regist(CoordListGenerator())

    def build(self):
        result = self._generate_recursive(self.base_conf.copy(), self.ctx)
        self.writer.save(result, NAME_RUNS_CONFIG, overwrite=True)
    
    def _generate_recursive(self, cfg: dict, ctx) -> dict:
        result = {}

        for field_name, field in cfg.items():
            if field_name == 'type':
                continue

            if isinstance(field, dict) and 'type' in field:
                result[field_name] = self.register.resolve(name=field_name, cfg=field, ctx=ctx)

            elif isinstance(field, dict) and 'type' not in field:
                result[field_name] = self._generate_recursive(field, ctx)

            else:
                result[field_name] = field

        return result


class RuntimeContext:
    def __init__(self):
        self.value : dict[str, any] = {}
        self.occupied: set[tuple[int, int]] = set()

    def set(self, key, value):
        self.value[key] = value

    def get(self, key):
        return self.value[key]