from abc import ABC, abstractmethod
from builder_base.builder import BaseBuilder

class BuilderEnv(BaseBuilder, ABC):

    @abstractmethod
    def build(self, env=None):
        pass