from abc import ABC, abstractmethod
from typing import Any

class PenaltyDeadRewardModelComponent(ABC):
    def __init__(self):
        self.value_penalty: float

    @abstractmethod
    def penalty(self, *args: Any, **kwargs: Any) -> float:
        pass

    def set_value_penalty(self, penalty):
        self.value_penalty = penalty