from net.base.feature_module import FeatureModule
from torch import nn    
import torch

class FeaturesAdapterCritic(FeatureModule):

    def __init__(self, multi_encoder, fusion):
        super().__init__()

        if multi_encoder.output_dim != fusion.input_dim:
            raise ValueError(f"")
        
        self._out_dim = fusion.output_dim

        self.multi = multi_encoder
        self.fusion = fusion

    @property
    def input_dim(self) -> int:
        return None
    
    @property
    def output_dim(self) -> int:
        return self._out_dim
    
    def forward(self, x_dict):
        if isinstance(x_dict, list):
            batch_size = len(x_dict)
            results = []
            for item in x_dict:
                features = self.multi(item)
                fused = self.fusion(features)
                results.append(fused)
            return torch.stack(results, dim=0)
        else:
            features = self.multi(x_dict)
            return self.fusion(features)