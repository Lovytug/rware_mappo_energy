import energy_system.charging_station as chs
import energy_system.energy_robot as er

from energy_system.energy_env import EnergyEnv, EnergyMultiRobotSystem, ChargingStationsMultiRobotSystem

from param_adapter.energy_system_adapter import EnergyMultiRobotSystemAdapter
from param_adapter.energy_system_adapter import ChargingStationsMultiRobotSystemAdapter
from param_adapter.energy_system_adapter import EnergyEnvAdapter

from util.config_file import ReadConfigFileSystem
from util.path import CONFIG_EPISODE_RUN
from util.global_var import NAME_RUNS_CONFIG

from observer.observer import EnvObserver

from priority.priority_compose import PriorityCompose


class BuilderEnergyMultiRobotSystem:

    from energy_system.base.cost_model import CostModelComponent
    from energy_system.base.penalty_model import PenaltyDeadRewardModelComponent

    def __init__(
            self,
            cost_model: CostModelComponent,
            penalty_model: PenaltyDeadRewardModelComponent
    ):
        self.cost_model = cost_model
        self.penalty_model = penalty_model

    def with_cost_action(self, system):
        self.cost_model.set_cost_action(
            noop=system.cost_NOOP,
            load=system.cost_LOAD,
            forword=system.cost_FORWORD,
            left=system.cost_LEFT,
            right=system.cost_RIGHT
        )

        return self
    
    def with_penalty(self, system):
        self.penalty_model.set_value_penalty(system.depletion_penalty_dead)

        return self

    def build(self, current_env, energy_env, data):
        adapter = EnergyMultiRobotSystemAdapter(data)
        system = adapter.extract()

        (self.with_cost_action(system)
         .with_penalty(system))
        
        composer = PriorityCompose()

        composer.register(
            er.EnergyRobotSelfObservation,
            energy_env=energy_env
        )

        composer.register(
            er.EnergyDeadAgentAction,
            energy_env=energy_env
        )

        composer.register(
            er.EnergyDynamicConsumptionAction,
            energy_env=energy_env,
            cost_model=self.cost_model
        )

        composer.register(
            er.EnergyRewardDepletionPenalty,
            energy_env=energy_env,
            penalty_model=self.penalty_model
        )

        composer.register(
            er.EnergyDeadResolver,
            energy_env=energy_env
        )

        return composer.build(current_env)
    

class BuilderChargingStationsMultiRobotSystem:

    from energy_system.base.charging_rate_model import ChargingRateModelComponent
    from energy_system.base.charging_reward_model import ChargeRewardModelComponent

    def __init__(
            self,
            rate_model: ChargingRateModelComponent,
            reward_model: ChargeRewardModelComponent
    ):
        self.rate_model = rate_model
        self.reward_model = reward_model
    
    def with_charge_rate(self, system):
        self.rate_model.set_charge_rate(system.charged_rate)

        return self

    def with_charge_reward(self, system):
        self.reward_model.set_max_energy(system.max_energy)
        self.reward_model.set_critical_threshoold(system.critical_threshold_procent)
        self.reward_model.set_bonus_coef(system.bonus_charge_coef_critical_threshold)
        self.reward_model.set_charge_reward(system.charge_reward)
        
        return self

    def build(self, current_env, energy_env, data):
        adapter = ChargingStationsMultiRobotSystemAdapter(data)
        system = adapter.extract()

        (self.with_charge_rate(system)
         .with_charge_reward(system))
        
        composer = PriorityCompose()

        composer.register(
            chs.ChargingStationRewardCharge,
            energy_env=energy_env,
            charge_reward=self.reward_model
        )

        composer.register(
            chs.AgentsOnChargingStation,
            energy_env=energy_env
        )

        composer.register(
            chs.ChargingDynamicAgent,
            energy_env=energy_env,
            charging_rate_model=self.rate_model
        )

        composer.register(
            chs.ChargingStationIsVisibility,
            energy_env=energy_env
        )

        return composer.build(current_env)


class BuilderEnergyEnv:
    def __init__(self):
        self.reader = ReadConfigFileSystem(CONFIG_EPISODE_RUN)
    
    def list_tuple_stations(self, stations: list[list[int, int]]):
        result: list[tuple[int, int]] = []
        for x, y in stations:
            result.append((x, y))
        
        return result

    def build(self, current_env, list_builders):
        data = self.reader.get(NAME_RUNS_CONFIG)

        adapter = EnergyEnvAdapter(data)

        system = adapter.extract()

        robot = EnergyMultiRobotSystem(system.n_agent, system.max_energy)
        stations = ChargingStationsMultiRobotSystem(
            self.list_tuple_stations(system.stations),
        )

        energy_env = EnergyEnv(robot, stations)

        register = EnvObserver()
        register.register(robot)
        register.register(stations)

        for b in list_builders:
            current_env = b.build(current_env, energy_env, data)

        return current_env, register