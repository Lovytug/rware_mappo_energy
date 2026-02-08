from abc import ABC, abstractmethod
from typing import Any

class ChargingRateModelComponent(ABC):
    def __init__(self):
        self._rate: float

    @abstractmethod
    def charge(self, *args: Any, **kwargs: Any):
        pass

    def set_charge_rate(self, value):
        self._rate = value