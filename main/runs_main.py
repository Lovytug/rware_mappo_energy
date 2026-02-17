import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)


import gymnasium as gym
import rware
from read_write_file.reader.implementation.reader_config import ReaderConfigJSON, ReaderConfigJSONRun
from read_write_file.writer.implementation.writer_config import WriterConfigJSON
from util.global_var import NAME_RUN_CONFIG_EVER_EPISODE
import environments.energy_env.builder.builder_config as BC_energy
import environments.base_env.builder.builder_conf_episode as BC_base
from environments.base_env.builder.builder_env import BuilderBaseEnv
from environments.energy_env.builder.builder_env import BuilderEnergyEnv
from environments.base.builder.builder_orchestra import BuidlerOrchestraConfig, BuidlerOrchestraEnv
from environments.base.features_env.provider.entity_repos import EntityRepository
from environments.base.features_env.provider.mock_provider import MockProvider
from environments.base.features_env.extract_features.agent_agent import AgentAgentRelationBlock, AgentAgentConfig
from environments.base.features_env.extract_features.agent_shelf import AgentShelfRelationBlock, AgentShelfConfig
from environments.base.features_env.extract_features.agent_goal import AgentGoalRelationBlock, AgentGoalConfig
from environments.base.features_env.extract_features.agent_charging_stations import AgentChargingStationRelationBlock, AgentChargingStationConfig
from environments.base.features_env.extract_features.relation_assembler import RelationAssembler
from main.actor_main import build_actor
from main.critic_main import build_critic
from MAPPO.police.mappo_police import Policy
from MAPPO.factory.factory import EposidyFactory
from MAPPO.trainer.trainer import MAPPOTrainer


reader_conf_base_env = ReaderConfigJSON(r"D:\Files\repos мои проекты\RL склад\environments\base_env\configuration\base_env.json")
reader_conf_energy_env = ReaderConfigJSON(r"D:\Files\repos мои проекты\RL склад\environments\energy_env\configuration\energy_env.json")
wtiter = WriterConfigJSON()

config_base = BC_base.BuilderEpisodeJSON(reader_conf_base_env, wtiter)
config_energy = BC_energy.BuilderEpisodeJSON(reader_conf_energy_env, wtiter)

orchestra_config = BuidlerOrchestraConfig([config_base, config_energy])

reader_run = ReaderConfigJSONRun()

builder_base = BuilderBaseEnv(reader_run)
builder_energy = BuilderEnergyEnv(reader_run)

orchestra_env = BuidlerOrchestraEnv([builder_base, builder_energy])


factory = EposidyFactory(
    builder_episdoe=orchestra_config,
    builder_env=orchestra_env
)

policy = Policy(build_actor())

trainer = MAPPOTrainer(
    factory=factory,
    policy=policy,
    critic=build_critic(),
)

trainer.train(
    num_updates=1000,
    rollout_len=512
)
