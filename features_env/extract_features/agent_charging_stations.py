from features_env.base.relation_block import BaseRelationBlock
from features_env.provider.entity_repos import EntityRepository
from features_env.base.features_batch import FeatureBatch
from dataclasses import dataclass
import numpy as np
import torch

@dataclass
class AgentChargingStationConfig:
    max_relations: int
    max_width: int
    max_height: int
    max_energy: int


class AgentChargingStationRelationBlock(BaseRelationBlock):

    FEATURES_DIM = 11

    relation_type = "agent_charging_station"

    def __init__(self, cfg: AgentChargingStationConfig):
        self.cfg = cfg


    def _build_features_vector(self, agent, charge):
        dx = (charge.x - agent.x) / self.cfg.max_width
        dy = (charge.y - agent.y) / self.cfg.max_height

        dist = np.sqrt(dx**2 + dy**2)
        
        return [
            agent.x/self.cfg.max_width, agent.y/self.cfg.max_height, 
            agent.direction/4.0, agent.carring_shelf, agent.energy/self.cfg.max_energy,

            charge.x/self.cfg.max_width, charge.y/self.cfg.max_height, charge.employed,

            dx, dy, dist
        ]
    
    
    def _generate_for_charging_station(self, agent, charging_stations):
        relation = []
        for charge in charging_stations:
            dx = (charge.x - agent.x)
            dy = (charge.y - agent.y)
            dist = np.sqrt(dx**2 + dy**2)

            vec = self._build_features_vector(agent, charge)

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
            relations = self._generate_for_charging_station(agent, repo.charging_stations)

            selected = self._select_top_n(relations=relations)

            batch = self._pad_with_mask(selected)

            all_features.append(batch.features)
            all_masks.append(batch.mask)

        return FeatureBatch(
            features=torch.cat(all_features, dim=0),
            mask=torch.cat(all_masks, dim=0)
        )