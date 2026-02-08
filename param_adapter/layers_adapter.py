from param_adapter.data_adapter import DataAdapter
from dataclasses import dataclass

@dataclass(frozen=True)
class LayersParams:
    width: int
    height: int

    gates: list[list[int, int]]
    shelves: list[list[int, int]]
    charging_stations: list[list[int, int]]

class LayersParamsAdapter(DataAdapter):

    def extract(self) -> LayersParams:
        env = self.cfg['environment']

        return LayersParams(
            width=env['width'],
            height=env['height'],

            gates=env['gates'],
            shelves=env['shelves'],

            charging_stations=self.cfg['energy_system']['stations']
        )