from dataclasses import dataclass

@dataclass
class AgentState:
    id: int
    x: int
    y: int
    direction: int
    carring_shelf: bool
    energy: float

@dataclass
class ShelfState:
    id: int
    x: int
    y: int
    request: bool

@dataclass
class GoalState:
    x: int
    y: int

@dataclass
class ChargingStationState:
    x: int
    y: int
    rate: float
    employed: bool


class MockProvider:

    def __init__(self, env, manager):
        self.warehouse = env.unwrapped
        self.manager = manager.snapshot()

    def get_agents(self) -> list[AgentState]:
        result = []
        levels_energy=self.manager.energies_ratio

        for i, agent in enumerate(self.warehouse.agents):
            result.append(AgentState(
                id=agent.id,
                x=agent.x,
                y=agent.y,
                direction=agent.dir.value,
                carring_shelf=agent.carrying_shelf is not None,
                energy=levels_energy[i]
            ))

        return result
    
    def get_shelves(self) -> list[ShelfState]:
        result = []
        for shelf in self.warehouse.shelfs:
            result.append(ShelfState(
                id=shelf.id,
                x=shelf.x,
                y=shelf.y,
                request=shelf in self.warehouse.request_queue
            ))

        return result
    
    def get_goals(self) -> list[GoalState]:
        result = []
        for x, y in self.warehouse.goals:
            result.append(GoalState(
                x=x,
                y=y
            ))

        return result
    
    def get_charging_stations(self) -> list[ChargingStationState]:
        result = []

        coords = self.manager.coords_charge_station
        rates = self.manager.charge_rates

        for i, (x, y) in enumerate(coords):
            employed = any(agent.x == x and agent.y == y for agent in self.warehouse.agents)
            result.append(ChargingStationState(
                x=x,
                y=y,
                rate=rates[i],
                employed=employed
            ))

        return result