from environments.energy_env.subsystem.subsystem import EnergySubsystem
from environments.energy_env.domain.energy_robot import MultiEnergyRobots
from environments.energy_env.domain.charging_station import MultiChargingStations
from environments.base.domain_storage.storage_sub import StorageSubsystem


class EnergyStorageSubsystem(StorageSubsystem[MultiEnergyRobots]):

    @property
    def robots(self) -> MultiEnergyRobots:
        return self._domain


class ChargingStorageSubsystem(StorageSubsystem[MultiChargingStations]):

    @property
    def stations(self) -> MultiChargingStations:
        return self._domain