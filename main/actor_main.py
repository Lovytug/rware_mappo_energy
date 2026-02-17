from net.actor.adapter import FeaturesAdapterActor
from net.actor.back_bone import BackBoneActor
from net.actor.head import PredictionHeadActor

from net.builders.builder_net import BuilderModelNet
from net.A2C.modular_policy import ModularPolicyValueNet


LEN_OBS = 73

def build_actor() -> ModularPolicyValueNet:
    out_in_adapter = 128
    adapter = FeaturesAdapterActor(in_dim=LEN_OBS, out_embending_dim=out_in_adapter)

    back_bone = BackBoneActor(input_dim=out_in_adapter, output_dim=32)

    head = PredictionHeadActor(in_embending_dim=32, output_dim=1)

    return BuilderModelNet.build(adapter=adapter, backbone=back_bone, head=head)