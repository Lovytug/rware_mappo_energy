from environments.base.builder.builder_env import BuilderEnv

from environments.energy_env.energy_env import EnergyEnv

from environments.energy_env.domain.energy_robot import MultiEnergyRobots
from environments.energy_env.domain.charging_station import MultiChargingStations

from environments.energy_env.subsystem import action_subsystem, dynamic_subsystem, observation_subsystem, termination_subsystem

from environments.base.domain_storage.storage_factory import StorageFactory
import environments.energy_env.domain.regist.regist_domain_extract

from environments.base.gym_wrapper_env import EnvWrapper

from environments.base.observer.observer import EnvObserver

from read_write_file.reader.base.reader_file import ReaderFile


class BuilderEnergyEnv(BuilderEnv):

    def __init__(self, reader_runs: ReaderFile):
        super().__init__()
        self.reader = reader_runs

    def build(self, env=None):
        if env is None:
            raise ValueError("Для построения НЕ Base env необходима исходная среда")
        
        domain_classes = [
            MultiEnergyRobots,
            MultiChargingStations,
        ]

        data = self.reader.read().data
        
        storages, domains = StorageFactory.build_storages_from_env(data, env, domain_classes)

        observer = EnvObserver()
        for domain in domains:
            observer.register(domain)

        all_list = storages + [
                action_subsystem.EnergyActionSubsystem(),
                dynamic_subsystem.EnergyDynamicSubsystem(),
                observation_subsystem.EnergyObservationSubsystem(),
                termination_subsystem.EnergyTerminationSubsystem()
            ]
        
        energy_env = EnergyEnv(all_list)

        return EnvWrapper(env, energy_env), observer