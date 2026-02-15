from environments.base.features_env.base.relation_block import BaseRelationBlock
from environments.base.features_env.provider.entity_repos import EntityRepository
from environments.base.features_env.base.features_batch import FeatureBatch

from dataclasses import dataclass
import numpy as np
import torch

@dataclass
class AgentAgentConfig:
    max_relations: int
    max_width: int
    max_height: int


class AgentAgentRelationBlock(BaseRelationBlock):

    FEATURES_DIM = 13

    relation_type = "agent_agent"

    def __init__(self, cfg: AgentAgentConfig):
        self.cfg = cfg


    def _build_features_vector(self, agent_1, agent_2):
        dx = (agent_2.x - agent_1.x) / self.cfg.max_width
        dy = (agent_2.y - agent_1.y) / self.cfg.max_height

        dist = np.sqrt(dx**2 + dy**2)
        
        return [
            agent_1.x/self.cfg.max_width, agent_1.y/self.cfg.max_height, 
            agent_1.direction/4.0, agent_1.carring_shelf, agent_1.energy,

            agent_2.x/self.cfg.max_width, agent_2.y/self.cfg.max_height, 
            agent_2.direction/4.0, agent_2.carring_shelf, agent_2.energy,
            
            dx, dy, dist
        ]
    

    def _generate_for_agent(self, agent, agents):
        relation = []
        
        for other in agents:
            if agent.id == other.id:
                    continue

            dx = (other.x - agent.x)
            dy = (other.y - agent.y)
            dist = np.sqrt(dx**2 + dy**2)

            vec = self._build_features_vector(agent, other)

            relation.append((dist, vec))

        return relation
    

    def _select_top_n(self, relations):
        relations.sort(key=lambda x: x[0])

        vectors = [vec for _, vec in relations]

        return vectors[:self.cfg.max_relations]
    

    def _pad_with_mask(self, vectors):
        n = self.cfg.max_relations
        m = self.FEATURES_DIM

        result = np.zeros((n, m), dtype=np.float32)
        mask = np.zeros(n, dtype=np.bool_)

        k = min(len(vectors), n)

        if k > 0:
            result[:k] = vectors[:k]
            mask[:k] = True

        return FeatureBatch(
            features=torch.tensor(result),
            mask=torch.tensor(mask)
        )
    
    
    def build(self, repo: EntityRepository):
        all_features = []
        all_masks = []

        for agent in repo.agents:
            relations = self._generate_for_agent(agent, repo.agents)

            selected = self._select_top_n(relations=relations)

            batch = self._pad_with_mask(selected)

            all_features.append(batch.features)
            all_masks.append(batch.mask)

        return FeatureBatch(
            features=torch.cat(all_features, dim=0),
            mask=torch.cat(all_masks, dim=0)
        )