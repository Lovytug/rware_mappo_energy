from param_adapter.data_adapter import DataAdapter
from dataclasses import dataclass

@dataclass(frozen=True)
class EnergyEnvParams:
    max_energy: float
    n_agent: int
    stations: list[list[int, int]]

class EnergyEnvAdapter(DataAdapter):

    def extract(self):
        return EnergyEnvParams(
            n_agent=self.cfg['environment']['agent']['count'],
            max_energy=self.cfg['energy_system']['agent']['max_energy'],
            stations=self.cfg['energy_system']['stations']
        )


@dataclass(frozen=True)
class ChargingStationsMultiRobotSystemParams:
    max_energy: float

    critical_threshold_procent: float
    bonus_charge_coef_critical_threshold: float
    charge_reward: float

    charged_rate: float
    stations: list[list[int, int]]


class ChargingStationsMultiRobotSystemAdapter(DataAdapter):

    def extract(self) -> ChargingStationsMultiRobotSystemParams:
        system = self.cfg['energy_system']

        return ChargingStationsMultiRobotSystemParams(
            max_energy = system['agent']['max_energy'],
            critical_threshold_procent=system['critical_threshold_procent'],
            charge_reward=system['charge_reward'],
            bonus_charge_coef_critical_threshold=system['bonus_charge_coef_critical_threshold'],

            charged_rate=system['charged_rate'],
            stations=system['stations']
        )
    

@dataclass(frozen=True)
class EnergyMultiRobotSystemParams:
    max_energy: int
    depletion_penalty_dead: float

    cost_NOOP: float
    cost_FORWORD: float
    cost_LOAD: float
    cost_LEFT: float
    cost_RIGHT: float

class EnergyMultiRobotSystemAdapter(DataAdapter):
    
    def extract(self) -> EnergyMultiRobotSystemParams:
        system = self.cfg['energy_system']
        agent_conf = system['agent']

        return EnergyMultiRobotSystemParams(
            max_energy=agent_conf['max_energy'],
            depletion_penalty_dead=agent_conf['depletion_penalty_dead'],

            cost_NOOP=agent_conf['cost_action']['NOOP'],
            cost_FORWORD=agent_conf['cost_action']['FORWARD'],
            cost_LOAD=agent_conf['cost_action']['LOAD'],
            cost_LEFT=agent_conf['cost_action']['LEFT'],
            cost_RIGHT=agent_conf['cost_action']['RIGHT']
        )