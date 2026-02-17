from environments.base.builder.builder_orchestra import BuidlerOrchestraEnv, BuidlerOrchestraConfig

from MAPPO.factory.build_relation_blocks import build_relation_blocks

from environments.base.features_env.provider.mock_provider import MockProvider
from environments.base.features_env.provider.env_state_provider import EnvStateProvider
from environments.base.features_env.provider.entity_repos import EntityRepository

from environments.base.features_env.extract_features.relation_assembler import RelationAssembler


class EpisodeContext:

    def __init__(self, env, assembler, repos):
        self.env = env
        self.assembler = assembler
        self.repos = repos


class EposidyFactory:

    def __init__(
            self,
            builder_episdoe: BuidlerOrchestraConfig,
            builder_env: BuidlerOrchestraEnv,
            relation_blocks_builder = build_relation_blocks
    ):
        
        self.builder_episdoe = builder_episdoe
        self.builder_env = builder_env
        self.relation_blocks_builder = relation_blocks_builder

    def create(self):

        self.builder_episdoe.build()

        env, reg = self.builder_env.build()
        
        obs, _ = env.reset()

        provider = MockProvider(env, reg)
        repos = EntityRepository(provider=provider)

        assembler = RelationAssembler(self.relation_blocks_builder(env))
        
        return EpisodeContext(env, assembler, repos)