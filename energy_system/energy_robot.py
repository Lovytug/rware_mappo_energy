import gymnasium as gym
import numpy as np
from gymnasium.spaces import Box

from energy_system.energy_env import EnergyEnv
from energy_system.base.cost_model import CostModelComponent
from energy_system.base.penalty_model import PenaltyDeadRewardModelComponent

from priority.priority import Priority


class EnergyRobotSelfObservation(Priority, gym.ObservationWrapper):
    priority = 1
    
    def __init__(self, current_env, energy_env : EnergyEnv):
        super().__init__(current_env)
        self.energy = energy_env

        new_spaces = []
        for spaces in self.observation_space:
            low = np.append(spaces.low, 0)
            high = np.append(spaces.high, self.energy.energy_robot.max_energy)
            new_spaces.append(Box(low, high, dtype=np.float32))

        self.observation_space = gym.spaces.Tuple(tuple(new_spaces))

    def reset(self, **kwargs):
        self.energy.reset()
        obs, info = self.env.reset(**kwargs)
        return self.observation(obs), info
    
    def observation(self, obs):
        return tuple(
            np.append(obs, self.energy.energy_robot.levels_energy[i])
            for i, obs in enumerate(obs)
        )
    

class EnergyDeadAgentAction(Priority, gym.ActionWrapper):
    priority = 2

    def __init__(self, current_env, energy_env : EnergyEnv):
        super().__init__(current_env)
        self.energy = energy_env
        self.NOOP = 0
    
    def action(self, action):
        mod_action = list(action)

        for i in range(len(action)):
            if self.energy.is_dead_agents[i]:
                mod_action[i] = self.NOOP

        return tuple(mod_action)


class EnergyDynamicConsumptionAction(Priority, gym.Wrapper):
    priority = 3

    def __init__(self, current_env, energy_env: EnergyEnv, cost_model: CostModelComponent):
        super().__init__(current_env)
        self.energy = energy_env
        self.cost_model = cost_model

    def step(self, action):
        obs, reward, term, trunc, info = self.env.step(action)
        
        levels_energy = self.energy.energy_robot.levels_energy.copy()
        for i in range(len(obs)):
            cost = self.cost_model.cost(action[i])
            levels_energy[i] = max(0.0, levels_energy[i] - cost)

        self.energy.energy_robot.levels_energy = levels_energy

        return obs, reward, term, trunc, info


class EnergyDeadResolver(Priority, gym.Wrapper):
    priority = 4

    def __init__(self, current_env, energy_env: EnergyEnv):
        super().__init__(current_env)
        self.energy = energy_env

    def step(self, action):
        obs, reward, term, trunc, info = self.env.step(action)

        levels_energy = self.energy.energy_robot.levels_energy.copy()
        dead = self.energy.is_dead_agents

        for i in range(len(levels_energy)):
            if levels_energy[i] == 0.0:
                dead[i] = True
            else:
                dead[i] = False

        if np.all(dead):
            term = True

        return obs, reward, term, trunc, info
        

class EnergyRewardDepletionPenalty(Priority, gym.Wrapper):
    priority = 5
    
    def __init__(self, current_env, energy_env: EnergyEnv, penalty_model: PenaltyDeadRewardModelComponent):
        super().__init__(current_env)
        self.energy = energy_env
        self.penalty = penalty_model

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)

        is_dead = self.energy.is_dead_agents
        for i in range(len(obs)):
            if is_dead[i]:
                reward[i] -= self.penalty.penalty()

        return obs, reward, terminated, truncated, info


