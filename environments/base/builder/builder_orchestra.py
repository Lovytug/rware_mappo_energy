from abc import ABC, abstractmethod
from builder_base.builder import BaseBuilder
from environments.base.builder.builder_env import BuilderEnv
from environments.base.builder.builder_conf import BuilderConfig, RuntimeContext
from environments.base.observer.observer import EnvObserver

class BuidlerOrchestra(BaseBuilder, ABC):

    @abstractmethod
    def build(self):
        pass


class BuidlerOrchestraConfig(BuidlerOrchestra):

    def __init__(self, builders_conf: list[BuilderConfig]):
        super().__init__()

        self.builders = builders_conf
        self.ctx = RuntimeContext()

    def build(self):

        for builder in self.builders:
            builder.build(self.ctx)


class BuidlerOrchestraEnv(BuidlerOrchestra):

    def __init__(self, builders_env: list[BuilderEnv]):
        super().__init__()

        self.builders = builders_env

    def build(self):

        env = None
        registers = EnvObserver()
        
        for builder in self.builders:
            env, register = builder.build(env)
            registers += register

        return env, registers
