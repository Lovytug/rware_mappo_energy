from net.base.feature_module import FeatureModule
from torch import nn

class PredictionHeadActor(FeatureModule):
    def __init__(self, in_embending_dim, output_dim=1):
        super().__init__()

        self._in_dim = in_embending_dim
        self._out_dim = output_dim

        self.head = nn.Linear(in_embending_dim, output_dim)

    @property
    def input_dim(self) -> int:
        return self._in_dim
    
    @property
    def output_dim(self) -> int:
        return self._out_dim
    
    def forward(self, x):
        return self.head(x)