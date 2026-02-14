from environments.energy_env.energy_env import EnergyEnv
from environments.energy_env.subsystem.subsystem import EnergySubsystem
from environments.energy_env.subsystem.storage import EnergyStorageSubsystem, ChargingStorageSubsystem

class EnergyDynamicSubsystem(EnergySubsystem):

    after = (EnergyStorageSubsystem,)

    def post_step(self, action: list[int], base_env, env: EnergyEnv):
        robots_storage: EnergyStorageSubsystem = env.get(EnergyStorageSubsystem)
        stations_storgae: ChargingStorageSubsystem = env.get(ChargingStorageSubsystem)

        robots = robots_storage.robots
        stations = stations_storgae.stations

        for i, robot in enumerate(robots.robots):
            if robot.is_discharged:
                continue

            robot.current_energy -= 1.0

            agent = base_env.unwrapped.agents[i]

            if (agent.x, agent.y) in stations.coords:
                id = stations.coords.index(agent.x, agent.y)
                robot.current_energy = min(
                    robot.max_energy,
                    robot.current_energy + stations.charge_rate[id]
                )


        return super().post_step(base_env, env)