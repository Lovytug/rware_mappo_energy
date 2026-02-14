from environments.base.extracter.data_env_extarctor import DataExtracterEnv
from dataclasses import dataclass
from typing import Union

@dataclass
class ChargingStationParams:
    stations: list[list[int, int]]
    charge_rate: Union[float, list[float]]


class ChargingStationExtracter(DataExtracterEnv):

    @staticmethod
    def extract(data, env=None) -> ChargingStationParams:
        energy_env = data['energy_env']

        return ChargingStationParams(
            stations=energy_env['stations'],
            charge_rate=energy_env['charge_rate']
        )