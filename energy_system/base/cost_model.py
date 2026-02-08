from abc import ABC, abstractmethod
from typing import Any

class CostModelComponent(ABC):
    def __init__(self):
        self.NOOP: float
        self.FORWORD: float
        self.LOAD: float
        self.LEFT: float
        self.RIGHT: float

    @abstractmethod
    def cost(self, action, *args: Any, **kwargs: Any) -> float:
        pass

    def set_cost_action(
            self,
            noop,
            load,
            forword,
            left,
            right
    ):
        self.NOOP = noop
        self.FORWORD = forword
        self.LOAD = load
        self.LEFT = left
        self.RIGHT = right