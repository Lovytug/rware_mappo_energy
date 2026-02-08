from energy_system.base.penalty_model import PenaltyDeadRewardModelComponent

class PenaltyDeadRewardModelV1(PenaltyDeadRewardModelComponent):

    def penalty(self, *args, **kwargs):
        return self.value_penalty