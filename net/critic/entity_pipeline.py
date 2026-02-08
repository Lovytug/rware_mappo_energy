from net.base.feature_module import FeatureModule
from net.critic.encode import EntityEncoder, SetEncoder
from torch import nn
from features_env.base.features_batch import FeatureBatch
import torch

class EntityPipeline(FeatureModule):

    def __init__(
            self,
            entity_encoder: EntityEncoder,
            set_encoder: SetEncoder
    ):
        super().__init__()

        self._input_dim = entity_encoder.input_dim
        self._output_dim = set_encoder.output_dim

        if entity_encoder.output_dim != set_encoder.input_dim:
            raise ValueError(f"Entity выход {entity_encoder.output_dim} должен быть равен SerEntity {set_encoder.input_dim}")
        
        self.encoder = entity_encoder
        self.set_encoder = set_encoder

    @property
    def input_dim(self):
        return self._input_dim

    @property
    def output_dim(self):
        return self._output_dim

    def forward(self, batch: FeatureBatch):
        x = self.encoder(batch.features)
        new_features = self.set_encoder(x, batch.mask)

        return FeatureBatch(new_features)
    

class MultiEntityEncoder(nn.Module):

    def __init__(self, pipelines: dict[str, EntityPipeline]):
        super().__init__()

        self.pipelines = nn.ModuleDict(pipelines)

        dims = {k: p.output_dim for k, p in pipelines.items()}

        self._output_dim = next(iter(dims.values()))

    @property
    def output_dim(self):
        return self._output_dim
    
    def forward(self, x_dict):
        return {
            k: pipe(x_dict[k]) for k, pipe in self.pipelines.items()
        }
    

class GroupFusion(FeatureModule):

    def __init__(self, latent_dim, pooling):
        super().__init__()

        self.pooling = pooling
        self._inpit_dim = latent_dim
        self._output_dim = latent_dim

    @property
    def input_dim(self) -> int:
        return self._inpit_dim
    
    @property
    def output_dim(self) -> int:
        return self._output_dim
    
    def forward(self, features_dict):
        tensor = [v.features for v in features_dict.values()]

        stacked = torch.stack(tensor, dim=0)

        return self.pooling(stacked)