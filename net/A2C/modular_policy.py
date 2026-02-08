from abc import ABC, abstractmethod
from torch import nn
from net.base.feature_module import FeatureModule

class ModularPolicyValueNet(nn.Module):
    def __init__(
            self,
            features_adapter: FeatureModule,
            back_bone: FeatureModule,
            head: FeatureModule
    ):
        super().__init__()

        self.adapter = features_adapter
        self.back_bone = back_bone
        self.head = head

        assert self.adapter.output_dim == self.back_bone.input_dim, \
            f"Несовпадение выхода из адапетера - {self.adapter.output_dim} и входа для тела - {self.back_bone.input_dim}"
        
        assert self.back_bone.output_dim == self.head.input_dim, \
            f"Несовпадение выхода из тела - {self.back_bone.output_dim} и входа для головы - {self.head.input_dim}"
        
    def forward(self, x):
        x = self.adapter(x)
        x = self.back_bone(x)
        x = self.head(x)
        return x
