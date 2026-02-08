from energy_system.base.charging_reward_model import ChargeRewardModelComponent

class ChargingRewardModelV1(ChargeRewardModelComponent):

    def reward(self, current_energy):
        value_critical_energy = self.max_energy * self.critical
        
        reward = 0
        if value_critical_energy >= current_energy:
            reward += self.charge_reward + self.charge_reward * self.bonus_coef
        else:
            reward += self.charge_reward

        return reward