from environments.base.features_env.extract_features.agent_agent import AgentAgentRelationBlock
from environments.base.features_env.extract_features.agent_shelf import AgentShelfRelationBlock
from environments.base.features_env.extract_features.agent_goal import AgentGoalRelationBlock
from environments.base.features_env.extract_features.agent_charging_stations import AgentChargingStationRelationBlock

from net.critic.encode import EntityEncoder, SetEncoder
from net.critic.pooling import AttentionPooling
from net.critic.entity_pipeline import EntityPipeline, GroupFusion, MultiEntityEncoder

from net.critic.embedding_adapter import FeaturesAdapterCritic
from net.critic.back_bones import BackBoneCritic
from net.critic.head import PredictionHeadCritic

from net.builders.builder_net import BuilderModelNet

def build_critic() -> BuilderModelNet:
    a_a = AgentAgentRelationBlock(None)
    a_s = AgentShelfRelationBlock(None)
    a_g = AgentGoalRelationBlock(None)
    a_c = AgentChargingStationRelationBlock(None)

    output_emb = 64
    agent_agent = EntityEncoder(a_a.FEATURES_DIM, output_emb)
    agent_shelf = EntityEncoder(a_s.FEATURES_DIM, output_emb)
    agent_goal = EntityEncoder(a_g.FEATURES_DIM, output_emb)
    agent_charging_station = EntityEncoder(a_c.FEATURES_DIM, output_emb)

    set_agent = SetEncoder(latent_dim=output_emb, pooling=AttentionPooling(output_emb))
    set_shelf = SetEncoder(latent_dim=output_emb, pooling=AttentionPooling(output_emb))
    set_goal = SetEncoder(latent_dim=output_emb, pooling=AttentionPooling(output_emb))
    set_chatging_station = SetEncoder(latent_dim=output_emb, pooling=AttentionPooling(output_emb))

    pipe_agent = EntityPipeline(agent_agent, set_agent)
    pipe_shelf = EntityPipeline(agent_shelf, set_shelf)
    pipe_goal = EntityPipeline(agent_goal, set_goal)
    pipe_charging_station = EntityPipeline(agent_charging_station, set_chatging_station)


    multi_enc = MultiEntityEncoder(
        {
            "agent_agent": pipe_agent,
            "agent_shelf": pipe_shelf,
            "agent_goal": pipe_goal,
            "agent_charging_station": pipe_charging_station
        }
    )

    fusion_dim = 64
    fusion = GroupFusion(fusion_dim, AttentionPooling(fusion_dim))

    output_dim = fusion_dim
    adapter = FeaturesAdapterCritic(multi_encoder=multi_enc, fusion=fusion)

    back_bone = BackBoneCritic(input_dim=output_dim, output_dim=64)

    head = PredictionHeadCritic(input_embedding_dim=64, output_dim=1)


    return BuilderModelNet().build(adapter=adapter, backbone=back_bone, head=head)