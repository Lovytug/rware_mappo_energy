from environments.base.extracter.data_env_extarctor import DataExtracterEnv
from environments.energy_env.domain.energy_robot import MultiEnergyRobots

from dataclasses import dataclass
from typing import Union


@dataclass
class EnergyRobotParams:
    n_agents: int
    max_energy: Union[float, list[float]]
    energy: Union[float, list[float], None] = None


class EnergyRobotExtracter(DataExtracterEnv):
    
    def extract(data, env=None) -> MultiEnergyRobots:
        energy = data['energy_env']
        n = env.unwrapped.n_agents

        max_energy = energy['agents']['max_energy']
        current_energy = energy['agents'].get('current_energy')

        if not isinstance(max_energy, list):
            max_energy = [max_energy] * n

        if current_energy is not None and not isinstance(current_energy, list):
            current_energy = [current_energy] * n

        return MultiEnergyRobots(
            n_agents=n,
            max_energy=max_energy,
            current_energy=current_energy
        )