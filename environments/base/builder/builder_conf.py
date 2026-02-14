from abc import ABC, abstractmethod
from builder_base.builder import BaseBuilder

class BuilderConfig(BaseBuilder, ABC):

    @abstractmethod
    def build(self):
        pass