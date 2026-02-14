from environments.base.extracter.data_env_extarctor import DataExtracterEnv
from dataclasses import dataclass
from typing import Union


@dataclass
class EnergyRobotParams:
    n_agents: int
    max_energy: Union[float, list[float]]
    energy: Union[float, list[float], None] = None


class EnergyRobotExtracter(DataExtracterEnv):
    
    @staticmethod
    def extract(data, env=None) -> EnergyRobotParams:
        energy = data['energy_env']

        return EnergyRobotParams(
            n_agents=env.unwrapped.n_agents,
            max_energy=energy['agents']['max_energy']
        )