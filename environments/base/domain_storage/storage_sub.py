from typing import Generic, TypeVar
from environments.base.domain_storage.domain import DomainModel
from environments.base.env_subsystem import EnvSubsystem


D = TypeVar("D", bound=DomainModel)

class StorageSubsystem(EnvSubsystem, Generic[D]):

    def __init__(self, domain: D):
        self._domain = domain

    @property
    def domain(self) -> D:
        return self._domain

    @property
    def domain_type(self):
        return type(self._domain)
