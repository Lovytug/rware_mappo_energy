from abc import ABC, abstractmethod
from torch import nn

class FeatureModule(nn.Module, ABC):

    @property
    @abstractmethod
    def input_dim(self) -> int:
        pass

    @property
    @abstractmethod
    def output_dim(self) -> int:
        pass