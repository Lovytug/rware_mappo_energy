from net.A2C.modular_policy import ModularPolicyValueNet

class Actor(ModularPolicyValueNet):
    
    def forward(self, x):
        x = self.adapter(x)
        x = self.back_bone(x)
        x = self.head(x)
        return x
