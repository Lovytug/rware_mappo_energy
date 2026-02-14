from typing import Any
from environments.base.domain_storage.domain import DomainModel

class DomainExtractorRegistry:

    _registry: dict[type[DomainModel], type] = {}

    @classmethod
    def register(cls, domain_cls: type[DomainModel], extractor_cls: type):
        cls._registry[domain_cls] = extractor_cls

    @classmethod
    def extract(cls, domain_cls: type[DomainModel], env: Any):
        extractor_cls = cls._registry.get(domain_cls)
        if extractor_cls is None:
            raise ValueError(f"No extractor registered for {domain_cls}")
        return extractor_cls.extract(env)
