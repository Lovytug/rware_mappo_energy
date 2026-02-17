from net.base.feature_module import FeatureModule
from net.A2C.modular_policy import ModularPolicyValueNet

class BuilderModelNet:
    
    @staticmethod
    def connect(a: FeatureModule, b: FeatureModule):
        if a.output_dim != b.input_dim:
            raise ValueError(f"Несоответствие вход и выходов {a.output_dim} -> {b.input_dim}")
        
    @staticmethod
    def build(adapter, backbone, head):
        BuilderModelNet.connect(adapter, backbone)
        BuilderModelNet.connect(backbone, head)

        return ModularPolicyValueNet(adapter, backbone, head)