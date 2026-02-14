from environments.energy_env.energy_env import EnergyEnv
from environments.energy_env.subsystem.subsystem import EnergySubsystem
from environments.energy_env.subsystem.storage import EnergyStorageSubsystem

class EnergyActionSubsystem(EnergySubsystem):

    after = (EnergyStorageSubsystem, )

    def pre_action(self, action: list[int], base_env, env: EnergyEnv):
        
        robots_storage: EnergyStorageSubsystem = env.get(EnergyStorageSubsystem)
        robots = robots_storage.robots

        new_actions = []

        for i, action in enumerate(action):
            if robots[i].is_discharged:
                new_actions.append(base_env.action_space[0])
            else:
                new_actions.append(action)

        return new_actions