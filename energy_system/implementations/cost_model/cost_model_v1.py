from energy_system.base.cost_model import CostModelComponent

class CostModelV1(CostModelComponent):

    def cost(self, action, *args, **kwargs):
        if action == 0:
            return self.NOOP
        elif action == 4:
            return self.LOAD
        elif action == 1:
            return self.FORWORD
        elif action == 2:
            return self.LEFT
        elif action == 3:
            return self.RIGHT