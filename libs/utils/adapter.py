class BusAdapter:
    def __init__(self, power, bus):
        self.p_set = power
        self.e_set = bus.average_efficiency()
        self.v_set = bus.average_voltage
        self.heat_capacity = bus.heat_capacity
        self.mass = bus.total_mass
        self.temperature=bus.initial_temperature
