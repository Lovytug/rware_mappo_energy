from dataclasses import dataclass

@dataclass
class AgentState:
    id: int
    x: int
    y: int
    direction: int
    carring_shelf: bool
    energy: int

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
    employed: bool


class MockProvider:

    def __init__(self, env, maneger):
        self.warehouse = env.unwrapped
        self.maneger = maneger.snapshot()

    def get_agents(self) -> list[AgentState]:
        result = []
        levels_energy=self.maneger.levels_energy

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

        stations = self.maneger.stations
        for x, y in stations:
            
            employed = any(agent.x == x and agent.y == y for agent in self.warehouse.agents)
            result.append(ChargingStationState(
                x=x,
                y=y,
                employed=employed
            ))

        return result