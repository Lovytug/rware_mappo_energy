from environments.base.features_env.base.relation_block import BaseRelationBlock
from environments.base.features_env.provider.entity_repos import EntityRepository

class RelationAssembler:

    def __init__(self, blocks: list[BaseRelationBlock]):
        self.blocks = blocks

    def build(self, repo: EntityRepository):
        result = {}

        for blocks in self.blocks:
            result[blocks.relation_type] = blocks.build(repo)

        return result