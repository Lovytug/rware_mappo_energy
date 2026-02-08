from typing import Protocol
from features_env.provider.mock_provider import AgentState, ShelfState, GoalState, ChargingStationState

class EnvStateProvider(Protocol):

    def get_agents(self) -> list[AgentState]:
        ...

    def get_shelves(self) -> list[ShelfState]:
        ...

    def get_goals(self) -> list[GoalState]:
        ...

    def get_charging_stations(self) -> list[ChargingStationState]:
        ...