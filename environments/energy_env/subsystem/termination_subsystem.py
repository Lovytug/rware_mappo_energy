from environments.energy_env.energy_env import EnergyEnv
from environments.energy_env.subsystem.subsystem import EnergySubsystem
from environments.energy_env.subsystem.storage import EnergyStorageSubsystem
from environments.energy_env.subsystem.dynamic_subsystem import EnergyDynamicSubsystem

class EnergyTerminationSubsystem(EnergySubsystem):

    after = (EnergyDynamicSubsystem,)

    def modify_reward(self, reward: list[float], base_env, env: EnergyEnv):
        robots_storage: EnergyStorageSubsystem = env.get(EnergyStorageSubsystem)
        
        robots = robots_storage.robots
        for i, robot in enumerate(robots.robots):
            if robot.is_discharged:
                reward[i] -= 1.0

        return reward
    
    def check_termination(self, terminated: bool, base_env, env: EnergyEnv):
        robots_storage: EnergyStorageSubsystem = env.get(EnergyStorageSubsystem)
        
        robots = robots_storage.robots

        if all(robots.discharged):
            return True
        
        return terminated