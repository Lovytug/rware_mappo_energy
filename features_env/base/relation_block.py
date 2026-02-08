from abc import ABC, abstractmethod
from features_env.provider.entity_repos import EntityRepository

class BaseRelationBlock(ABC):

    relation_type: str

    @abstractmethod
    def build(self, repo: EntityRepository):
        pass