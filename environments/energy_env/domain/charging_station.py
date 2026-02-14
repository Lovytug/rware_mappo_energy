from __future__ import annotations

from  dataclasses import dataclass
from typing import Union
from environments.base.domain_storage.domain import DomainModel


@dataclass
class ChargingStation:
    id_charging_station: int
    coord: tuple[int, int]
    charge_rate: float


class MultiChargingStations(DomainModel):

    def __init__(
            self,
            coords: list[tuple[int, int]],
            charge_rates: Union[float, list[float]]
    ):
        self._count_stations = len(coords)

        if isinstance(charge_rates, float):
            self.charge_rate_float(charge_rates)
        
        elif isinstance(charge_rates, list):
            self.charge_rate_list(charge_rates)

        else:
            raise TypeError(f"Существет недопустимый тип для charge_rate")
        
        self._station = [ChargingStation(
            id=i,
            coord=coords[i],
            charge_rate=self._charge_rates[i]
        )
        for i in range(self._count_stations)
        ]


    def charge_rate_float(self, charge_rates: float):
        if charge_rates <= 0.0:
            raise ValueError(f"Скорость зарядки станции не может быть отрициательной или нулем")
        else:
            self._charge_rates = [charge_rates for _ in range(self._count_stations)]


    def charge_rate_list(self, charge_rates: list[float]):
        if len(charge_rates) != self._count_stations:
            raise ValueError(f"Список из 'скорость зарядки' должен быть длинной {self._count_stations}. Пришло {len(charge_rates)}")
        else:
            for rate in charge_rates:
                if rate <= 0.0:
                    raise ValueError(f"Скорость зарядки станции не может быть отрициательной или нулем")
                else:
                    self._charge_rates.append(rate)


    def reset(self):
        pass


    @property
    def stations(self) -> list[ChargingStation]:
        return self._station
    
    @property
    def coords(self) -> list[tuple[int, int]]:
        return [r.coord for r in self._station]
    
    @property
    def coord(self) -> CoordView:
        return CoordView(self._station)
    
    @property
    def charge_rates(self) -> list[float]:
        return [r.charge_rate for r in self._station]
    
    @property
    def charge_rate(self) -> ChargeRateView:
        return ChargeRateView(self._station)
    

    def __getitem__(self, idx: int) -> ChargingStation:
        return self._station[idx]
    
    def __len__(self) -> int:
        return self._count_stations
    

class CoordView:

    def __init__(self, stations: list[ChargingStation]):
        self._stations = stations

    def __getitem__(self, idx: Union[int, slice]) -> Union[float, list[float]]:
        if isinstance(idx, int):
            if not 0 <= idx < len(self._stations):
                raise IndexError(f"Индекс взятый для координат: {idx} недопустим в диапозоне \
                                 [0, {len(self._stations)-1}]")
            return self._stations[idx].coord
        
        elif isinstance(idx, slice):
            return [r.coord for r in self._stations[idx]]
        
        else:
            raise TypeError(f"Индекс или срез допустимы для взятия координат")
        

class ChargeRateView:

    def __init__(self, stations: list[ChargingStation]):
        self._stations = stations

    def __getitem__(self, idx: Union[int, slice]) -> Union[float, list[float]]:
        if isinstance(idx, int):
            if not 0 <= idx < len(self._stations):
                raise IndexError(f"Индекс взятый для скорости зарядки: {idx} недопустим в диапозоне \
                                 [0, {len(self._stations)-1}]")
            return self._stations[idx].charge_rate
        
        elif isinstance(idx, slice):
            return [r.charge_rate for r in self._stations[idx]]
        
        else:
            raise TypeError(f"Индекс или срез допустимы для взятия скорости зарядки")