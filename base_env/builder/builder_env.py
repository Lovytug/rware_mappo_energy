from rware.warehouse import Warehouse

from base_env.extracter_data.warehouse import WarehouseExtracter
from base_env.builder.builder_layer import BuilderLayer

from builder_base.builder import BaseBuilder

from read_write_file.reader.base.reader_file import ReaderFile


class BuilderBaseEnv(BaseBuilder):

    def __init__(self, reader_runs: ReaderFile):
        super().__init__()
        self.reader = reader_runs


    def build(self):
        data = self.reader.read()
        builder_layer = BuilderLayer(data)

        params = WarehouseExtracter().extract(data)

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

            layout=builder_layer.build()
        )