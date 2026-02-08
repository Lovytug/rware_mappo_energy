from net.base.feature_module import FeatureModule
from torch import nn

class FeaturesAdapterActor(FeatureModule):

    def __init__(self, in_dim, out_embending_dim):
        super().__init__()

        self._out_dim = out_embending_dim
        
        self.adapter = nn.Linear(in_dim, out_embending_dim)

    @property
    def input_dim(self) -> int:
        return None
    
    @property
    def output_dim(self) -> int:
        return self._out_dim
    
    def forward(self, x):
        return self.adapter(x)
