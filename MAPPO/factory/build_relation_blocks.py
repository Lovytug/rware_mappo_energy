from environments.base.features_env.extract_features.agent_agent import AgentAgentRelationBlock, AgentAgentConfig
from environments.base.features_env.extract_features.agent_shelf import AgentShelfRelationBlock, AgentShelfConfig
from environments.base.features_env.extract_features.agent_goal import AgentGoalRelationBlock, AgentGoalConfig
from environments.base.features_env.extract_features.agent_charging_stations import AgentChargingStationRelationBlock, AgentChargingStationConfig

def build_relation_blocks(env):

    height, width = env.unwrapped.grid_size

    return[

        AgentAgentRelationBlock(AgentAgentConfig(
        max_relations=4, max_height=height, max_width=width
        )),

        AgentShelfRelationBlock(AgentShelfConfig(
        max_relations=7, max_height=height, max_width=width
        )),

        AgentGoalRelationBlock(AgentGoalConfig(
        max_relations=5, max_height=height, max_width=width
        )),

        AgentChargingStationRelationBlock(AgentChargingStationConfig(
        max_relations=5, max_height=height, max_width=width
        )),
    ]