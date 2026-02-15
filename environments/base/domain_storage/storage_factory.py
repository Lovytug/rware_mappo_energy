from typing import Any
from environments.base.domain_storage.domain_registry_extracter import DomainExtractorRegistry
from environments.base.domain_storage.domain import DomainModel
from environments.base.env_subsystem import EnvSubsystem

class StorageFactory:

    _registry: dict[type[DomainModel], type[EnvSubsystem]] = {}

    @classmethod
    def register(cls, domain_cls: type[DomainModel], storage_cls: type[EnvSubsystem]):
        cls._registry[domain_cls] = storage_cls

    @classmethod
    def build_storages_from_env(cls, data, env: Any, domain_classes: list[type[DomainModel]]):
        storages = []
        domains = []
        for domain_cls in domain_classes:
            
            domain_instance = DomainExtractorRegistry.extract(domain_cls, data, env)
            domains.append(domain_instance)

            storage_cls = cls._registry.get(domain_cls)
            if storage_cls is None:
                raise ValueError(f"No storage registered for {domain_cls}")
            storages.append(storage_cls(domain_instance))

        return storages, domains
