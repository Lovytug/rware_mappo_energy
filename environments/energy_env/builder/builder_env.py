from environments.base.builder.builder_env import BuilderEnv

from environments.energy_env.energy_env import EnergyEnv

from environments.energy_env.domain.energy_robot import MultiEnergyRobots
from environments.energy_env.domain.charging_station import MultiChargingStations

from environments.energy_env.subsystem import action_subsystem, dynamic_subsystem, observation_subsystem, termination_subsystem

from environments.base.domain_storage.storage_factory import StorageFactory
import environments.energy_env.domain.regist.regist_domain_extract

from environments.base.gym_wrapper_env import EnvWrapper

class BuilderEnergyEnv(BuilderEnv):

    def __init__(self):
        super().__init__()

    def build(self, env=None):
        if env is None:
            raise ValueError("Для построения НЕ Base env необходима исходная среда")
        
        domain_classes = [
            MultiEnergyRobots,
            MultiChargingStations,
        ]

        storages = StorageFactory.build_storages_from_env(env, domain_classes)

        energy_env = EnergyEnv([
            storages +
            [
                action_subsystem.EnergyActionSubsystem(),
                dynamic_subsystem.EnergyDynamicSubsystem(),
                observation_subsystem.EnergyObservationSubsystem(),
                termination_subsystem.EnergyTerminationSubsystem()
            ]
        ])

        return EnvWrapper(env, energy_env)