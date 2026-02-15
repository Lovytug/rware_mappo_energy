from __future__ import annotations

from typing import Union
from dataclasses import dataclass
from environments.base.domain_storage.domain import DomainModel
from environments.base.observer.decor_observe import observe

@dataclass
class EnergyRobot:
    id: int
    max_energy: float
    current_energy: float

    @property
    def is_discharged(self) -> bool:
        return self.current_energy <= 1e-6
    
    @property
    def current_energy_ratio(self) -> float:
        return self.current_energy / self.max_energy


class MultiEnergyRobots(DomainModel):

    def __init__(
            self,
            n_agents: int,
            max_energy: Union[float, list[float]],
            current_energy: Union[float, list[float], None] = None
    ):
        self._n_agents = n_agents

        if isinstance(max_energy, list) and isinstance(current_energy, list):
            self.max_and_current_energy_list(max_energy, current_energy)

        elif isinstance(max_energy, list):
            self.max_energy_list(max_energy, current_energy)

        elif isinstance(current_energy, list):
            self.current_energy_list(max_energy, current_energy)

        else:
            raise TypeError(f"Существуют недопустимые типы для max_energy и/или current_energy")
        
        self._robots = [EnergyRobot(
            id=i,
            max_energy=self._max_energy[i],
            current_energy=self._current_energy[i]
        )
        for i in range(self._n_agents)
        ]
            

    def max_and_current_energy_list(self, max_energy: list[float], current_energy: list[float]):
        if len(max_energy) != self._n_agents and len(current_energy) != self._n_agents:
            raise ValueError(f"Подаваемые списки max_energy size: {len(max_energy)} \
                                 и current_energy size: {len(current_energy)} \
                                    должны быть равные кол-ву агентов size: {self._n_agents}")
        
        self._max_energy = max_energy
        self._current_energy = [min(current, max_current) 
                                for max_current, current in zip(max_energy, current_energy)]


    def max_energy_list(self, max_energy: list[float], current_energy: Union[float, None]):
        if len(max_energy) != self._n_agents:
            raise ValueError(f"Подаваемый список max_energy size: {len(max_energy)} \
                                    должен быть равен кол-ву агентов size: {self._n_agents}")
        
        self._max_energy = max_energy
        if current_energy is None:
            self._current_energy = [max_energy[i] for i in range(self._n_agents)]
        else:
            current_energy = min(current_energy, min(max_energy))
            self._current_energy = [current_energy for _ in range(self._n_agents)]


    def current_energy_list(self, max_energy: float, current_energy: list[float]):
        if len(current_energy) != self._n_agents:
            raise ValueError(f"Подаваемый список current_energy size: {len(current_energy)} \
                                    должен быть равен кол-ву агентов size: {self._n_agents}")
        
        if max_energy is None:
            raise ValueError(f"max energy не может быть не задан")
        
        self._max_energy = [max_energy for _ in range(self._n_agents)]
        self._current_energy = [min(current, max_energy) for current in current_energy]


    def reset(self):
        for i in range(self._n_agents):
            self._robots[i].current_energy = self._robots[i].max_energy


    @property
    def robots(self) -> list[EnergyRobot]:
        return self._robots

    @property
    def energies(self) -> list[float]:
        return [r.current_energy for r in self._robots]
    
    @property
    def energy(self) -> CurrentEnergyView:
        return CurrentEnergyView(self._robots)
    
    @property
    def max_energies(self) -> list[float]:
        return [r.max_energy for r in self._robots]
    
    @property
    def max_energy(self) -> MaxEnergyView:
        return MaxEnergyView(self._robots)
    
    @observe
    def energies_ratio(self) -> list[float]:
        return [r.current_energy_ratio for r in self._robots]
    
    @property
    def energy_ratio(self) -> CurrentEnergyRatioView:
        return CurrentEnergyRatioView(self._robots)
    
    @property
    def discharged(self) -> list[bool]:
        return [r.is_discharged for r in self._robots]


    def __getitem__(self, idx: int) -> EnergyRobot:
        return self._robots[idx]
    
    def __len__(self) -> int:
        return self._n_agents
    

class CurrentEnergyView:

    def __init__(self, robots: list[EnergyRobot]):
        self._robots = robots

    def __getitem__(self, idx: Union[int, slice]) -> Union[float, list[float]]:
        if isinstance(idx, int):
            if not 0 <= idx < len(self._robots):
                raise IndexError(f"Индекс взятый для энергии: {idx} недопустим в диапозоне \
                                 [0, {len(self._robots)-1}]")
            return self._robots[idx].current_energy
        
        elif isinstance(idx, slice):
            return [r.current_energy for r in self._robots[idx]]
        
        else:
            raise TypeError(f"Индекс или срез допустимы для взятия энергии")
        

class MaxEnergyView:

    def __init__(self, robots: list[EnergyRobot]):
        self._robots = robots

    def __getitem__(self, idx: Union[int, slice]) -> Union[float, list[float]]:
        if isinstance(idx, int):
            if not 0 <= idx < len(self._robots):
                raise IndexError(f"Индекс взятый для максимальной энергии: {idx} недопустим в диапозоне \
                                 [0, {len(self._robots)-1}]")
            return self._robots[idx].max_energy
        
        elif isinstance(idx, slice):
            return [r.max_energy for r in self._robots[idx]]
        
        else:
            raise TypeError(f"Индекс или срез допустимы для взятия максимальной энергии")
        

class CurrentEnergyRatioView:

    def __init__(self, robots: list[EnergyRobot]):
        self._robots = robots

    def __getitem__(self, idx: Union[int, slice]) -> Union[float, list[float]]:
        if isinstance(idx, int):
            if not 0 <= idx < len(self._robots):
                raise IndexError(f"Индекс взятый для нормированной энергии: {idx} недопустим в диапозоне \
                                 [0, {len(self._robots)-1}]")
            return self._robots[idx].current_energy_ratio
        
        elif isinstance(idx, slice):
            return [r.current_energy_ratio for r in self._robots[idx]]
        
        else:
            raise TypeError(f"Индекс или срез допустимы для взятия нормированной энергии")