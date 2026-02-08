from abc import ABC, abstractmethod

class ChargeRewardModelComponent(ABC):
    def __init__(self):
        self.max_energy: float
        self.charge_reward: float
        self.critical: float
        self.bonus_coef: float

    @abstractmethod
    def reward(self, current_energy):
        pass

    def set_max_energy(self, value):
        self.max_energy = value

    def set_charge_reward(self, value):
        self.charge_reward = value
    
    def set_critical_threshoold(self, value):
        self.critical = value

    def set_bonus_coef(self, value):
        self.bonus_coef = value