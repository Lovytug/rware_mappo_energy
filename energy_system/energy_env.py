import numpy as np
from observer.decor_observe import observe

class EnergyMultiRobotSystem:
    def __init__(
            self,
            n_agents: int, 
            max_energy: float
    ):
        self._max_energy = max_energy
        self._n_agents = n_agents
        self._energy = np.full(n_agents, max_energy, dtype=np.float32)

    @observe
    def max_energy(self) -> float:
        return self._max_energy
    
    @observe
    def n_agent(self) -> int:
        return self._n_agents
    
    @observe
    def levels_energy(self) -> np.ndarray:
        return self._energy
    
    @levels_energy.setter
    def levels_energy(self, update):
        if isinstance(update, list):
            update = np.array(update, dtype=np.float32)
        elif not isinstance(update, np.ndarray):
            raise TypeError("в levels_energy может подаваться или list или ndarray")
        
        if update.shape != self._energy.shape:
            raise ValueError(f"Размер массива подаваемый в levels_energy должен совпадать по кличеству агентов. Подано {update.shape}, а должно {self._energy}")
        self._energy[:] = update
    

class ChargingStationsMultiRobotSystem:
    def __init__(
            self,
            stations: list[tuple[int, int]],
    ):
        self._stations = set(stations)

    @observe
    def stations(self) -> list[tuple[int, int]]:
        return self._stations


class EnergyEnv:
    def __init__(
            self, 
            energy_robots: EnergyMultiRobotSystem, 
            charging_station: ChargingStationsMultiRobotSystem
    ):
        self.energy_robot = energy_robots
        self.charging_station = charging_station

        self.is_dead_agents = np.full(energy_robots.n_agent, 0, np.int8)
        self.is_charging_agents = np.full(energy_robots.n_agent, 0, np.int8)

    def reset(self):
        self.is_dead_agents[:] = False
        self.is_charging_agents[:] = False
        self.energy_robot._energy[:] = self.energy_robot.max_energy