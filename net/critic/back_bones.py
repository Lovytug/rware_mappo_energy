from net.base.feature_module import FeatureModule
from torch import nn

class BackBoneCritic(FeatureModule):
    def __init__(self, input_dim, output_dim, hidden_dims=[128, 128]):
        super().__init__()
        self._in_dim = input_dim
        self._out_dim = output_dim

        self.net = nn.Sequential()
        local_input = input_dim
        for hid in hidden_dims:
            self.net.append(
                nn.Sequential(
                    nn.Linear(local_input, hid),
                    nn.GELU()
                )
            )
            local_input = hid

        self.net.append(nn.Linear(hidden_dims[-1], output_dim))

    @property
    def input_dim(self) -> int:
        return self._in_dim
    
    @property
    def output_dim(self) -> int:
        return self._out_dim
    
    def forward(self, x):
        return self.net(x)