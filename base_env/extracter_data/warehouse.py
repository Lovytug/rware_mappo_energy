from extract_data_file.data_extracter import DataExtracter
from dataclasses import dataclass


@dataclass(frozen=True)
class WarehouseParams:
    shelf_columns: int
    shelf_rows: int
    column_height: int

    n_agents: int
    sensor_range: int
    msg_bits: int

    request_queue_size: int
    max_inactivity_steps: int
    max_steps: int
    reward_type: str


class WarehouseExtracter(DataExtracter):

    @staticmethod
    def extract(self, data) -> WarehouseParams:
        env = data['environment']
        deriver = WarehouseParamDeriver(env)

        shelf_columns, shelf_rows, column_height = deriver.derive_geometry()

        return WarehouseParams(
            shelf_columns=shelf_columns,
            shelf_rows=shelf_rows,
            column_height=column_height,

            n_agents=env['agent']['count'],
            sensor_range=env['agent']['radius_visible'],
            msg_bits=env['other']['msg_bits'],

            request_queue_size=min(env['other']['request_queue_size'], deriver.derive_request_queue_size()),
            max_inactivity_steps=env['other']['max_inactivity_steps'],
            max_steps=env['other']['max_steps'],
            reward_type=env['other']['reward_type']
        )
    

class WarehouseParamDeriver:
    """
    Отвечает ТОЛЬКО за вывод параметров,
    которые rware требует, но пользователь не задаёт явно
    """

    def __init__(self, env_cfg: dict):
        self.env_cfg = env_cfg

    def derive_geometry(self) -> tuple[int, int, int]:
        shelves = self.env_cfg["shelves"]

        if not shelves:
            return 1, 1, 1

        xs = [x for x, _ in shelves]
        ys = [y for _, y in shelves]

        shelf_columns = max(xs) + 1
        shelf_rows = max(ys) + 1
        column_height = 1

        return shelf_columns, shelf_rows, column_height

    def derive_request_queue_size(self) -> int:
        return max(1, len(self.env_cfg["shelves"]))
