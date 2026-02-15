from environments.base.extracter.data_env_extarctor import DataExtracterEnv
from environments.energy_env.domain.charging_station import MultiChargingStations
from dataclasses import dataclass
from typing import Union


@dataclass
class ChargingStationParams:
    stations: list[list[int, int]]
    charge_rate: Union[float, list[float]]


class ChargingStationExtracter(DataExtracterEnv):

    @staticmethod
    def extract(data, env=None) -> MultiChargingStations:
        energy_env = data['energy_env']

        coords = [tuple(c) for c in energy_env['stations']]
        charge_rate = energy_env['charge_rate']

        return MultiChargingStations(
            coords=coords,
            charge_rates=charge_rate
        )