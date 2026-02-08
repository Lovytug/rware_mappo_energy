from net.base.feature_module import FeatureModule
from torch import nn

class EntityEncoder(FeatureModule):

    def __init__(self, input_dim: int, output_dim: int, hidden_dim = [128, 64]):
        super().__init__()

        self._input_dim = input_dim
        self._output_dim = output_dim

        self.net = nn.Sequential()
        local_input = input_dim
        for hid in hidden_dim:
            self.net.append(
                nn.Sequential(
                    nn.Linear(local_input, hid),
                    nn.GELU()
                )
            )
            local_input = hid

    @property
    def input_dim(self) -> int:
        return self._input_dim
    
    @property
    def output_dim(self) -> int:
        return self._output_dim
    
    def forward(self, x):
        return self.net(x)
    

class SetEncoder(FeatureModule):

    def __init__(self, latent_dim, pooling):
        super().__init__()

        self._input_dim = latent_dim
        self._output_dim = latent_dim

        self.pooling = pooling
        self.post = nn.Linear(latent_dim, latent_dim)

    @property
    def input_dim(self):
        return self._input_dim
    
    @property
    def output_dim(self):
        return self._output_dim
    
    def forward(self, x, mask=None):
        x = self.pooling(x, mask)
        return self.post(x)