import gymnasium as gym
import numpy as np
from gymnasium.spaces import Box

from energy_system.energy_env import EnergyEnv
from energy_system.base.charging_rate_model import ChargingRateModelComponent
from energy_system.base.charging_reward_model import ChargeRewardModelComponent

from priority.priority import Priority


class ChargingStationIsVisibility(Priority, gym.ObservationWrapper):
    priority = 1

    def __init__(self, current_env, energy_env: EnergyEnv):
        super().__init__(current_env)
        self.energy = energy_env

        new_spaces = []
        for spaces in self.env.observation_space:
            low = np.append(spaces.low, 0)
            high = np.append(spaces.high, 1)

            new_spaces.append(Box(low, high, dtype=np.int8))

        self.observation_space = gym.spaces.Tuple(tuple(new_spaces))

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        return self.observation(obs), info

    def observation(self, obs):
        stations = self.energy.charging_station.stations
        new_obs = []
        for i, agent in enumerate(self.env.unwrapped.agents):
            ax, ay = agent.x, agent.y
            visible = any(
                abs(ax - sx) + abs(ay - sy) <= self.env.unwrapped.sensor_range
                for (sx, sy) in stations
            )
            new_obs.append(np.append(obs[i], int(visible)))
        return tuple(new_obs)
    
class AgentsOnChargingStation(Priority, gym.Wrapper):
    priority = 2

    def __init__(self, current_env, energy_env: EnergyEnv):
        super().__init__(current_env)
        self.energy = energy_env

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)

        stations = self.energy.charging_station.stations
        for i, agent in enumerate(self.env.unwrapped.agents):
            if (agent.x, agent.y) in stations:
                self.energy.is_charging_agents[i] = True
            else:
                self.energy.is_charging_agents[i] = False

        return obs, reward, terminated, truncated, info
    

class ChargingDynamicAgent(Priority, gym.Wrapper):
    priority = 3

    def __init__(self, current_env, energy_env: EnergyEnv, charging_rate_model: ChargingRateModelComponent):
        super().__init__(current_env)
        self.energy = energy_env
        self.rate = charging_rate_model

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)

        levels_energy = self.energy.energy_robot.levels_energy.copy()
        is_charging = self.energy.is_charging_agents
        max_energy = self.energy.energy_robot.max_energy
        for i in range(len(obs)):
            if is_charging[i]:
                levels_energy[i] = np.clip(
                    levels_energy[i] + self.rate.charge(), 
                    0.0,
                    max_energy
                ) 

        self.energy.energy_robot.levels_energy = levels_energy
        
        return obs, reward, terminated, truncated, info


class ChargingStationRewardCharge(Priority, gym.Wrapper):
    priority = 4

    def __init__(self, current_env, energy_env: EnergyEnv, charge_reward: ChargeRewardModelComponent):
        super().__init__(current_env)
        self.energy = energy_env
        self.charge_reward = charge_reward

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)

        levels_energy = self.energy.energy_robot.levels_energy.copy()
        is_charging = self.energy.is_charging_agents
        max_energy = self.energy.energy_robot.max_energy
        for i in range(len(obs)):
            if is_charging[i]:
                if levels_energy[i] >= max_energy:
                    reward[i] -= self.charge_reward.reward(levels_energy[i]) * 0.1
                else:
                    reward[i] += self.charge_reward.reward(levels_energy[i])

        return obs, reward, terminated, truncated, info

