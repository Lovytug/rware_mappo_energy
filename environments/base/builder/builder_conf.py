from abc import ABC, abstractmethod
from builder_base.builder import BaseBuilder


class RuntimeContext:
    
    def __init__(self):
        self.value : dict[str, any] = {}
        self.occupied: set[tuple[int, int]] = set()

    def set(self, key, value):
        self.value[key] = value

    def get(self, key):
        return self.value[key]
    

class BuilderConfig(BaseBuilder, ABC):

    @abstractmethod
    def build(self, ctx: RuntimeContext):
        pass