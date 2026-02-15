from environments.energy_env.energy_env import EnergyEnv
from environments.energy_env.subsystem.subsystem import EnergySubsystem
from environments.energy_env.subsystem.storage import EnergyStorageSubsystem
from environments.energy_env.subsystem.dynamic_subsystem import EnergyDynamicSubsystem, ChargingStorageSubsystem
from typing import Any
import numpy as np

class EnergyObservationSubsystem(EnergySubsystem):

    after = (EnergyDynamicSubsystem,)

    def modify_obs(self, obs, base_env, env: EnergyEnv):
        robots_storage: EnergyStorageSubsystem = env.get(EnergyStorageSubsystem)
        stations_storgae: ChargingStorageSubsystem = env.get(ChargingStorageSubsystem)

        robots = robots_storage.robots
        stations = stations_storgae.stations

        new_obs = []

        agents = base_env.unwrapped.agents
        for i, agent_obs in enumerate(obs):
            (ax, ay) = (agents[i].x, agents[i].y)

            visible = any(
                abs(ax - sx) + abs(ay - sy) <= base_env.unwrapped.sensor_range
                for (sx, sy) in stations.coords_charge_station
            )

            extend_obs = np.concatenate([
                agent_obs,
                [float(robots.energy[i])],
                [1.0 if visible else 0.0]
            ])

            new_obs.append(extend_obs)

        return tuple(new_obs)