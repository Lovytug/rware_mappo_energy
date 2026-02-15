from environments.base.features_env.provider.env_state_provider import EnvStateProvider

class EntityRepository:

    def __init__(self, provider: EnvStateProvider):
        self.provider = provider
        self.refresh()

    def refresh(self):
        self.agents = self.provider.get_agents()
        self.shelves = self.provider.get_shelves()
        self.goals = self.provider.get_goals()
        self.charging_stations = self.provider.get_charging_stations()