from net.base.feature_module import FeatureModule
from torch import nn

class PredictionHeadCritic(FeatureModule):
    
    def __init__(self, input_embedding_dim, output_dim = 1):
        super().__init__()

        self._input_dim = input_embedding_dim
        self._output_dim = output_dim

        self.linear = nn.Linear(input_embedding_dim, output_dim)

    @property
    def output_dim(self):
        return self._output_dim
    
    @property
    def input_dim(self) -> int:
        return self._input_dim
    
    def forward(self, x):
        return self.linear(x)