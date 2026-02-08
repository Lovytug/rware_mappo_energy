from energy_system.base.charging_rate_model import ChargingRateModelComponent

class ChargingRateModelV1(ChargingRateModelComponent):

    def charge(self, *args, **kwargs):
        return self._rate