class CustomBus:
    typename = 'Bus'
    def __init__(self, name, valueEngine, num_of_gen=1, num_of_load=1, init_temp=25, heat_cap=500):
        self.name = name
        self.initial_temperature = init_temp
        self.heat_capacity = heat_cap
        self.VE = valueEngine
        self.average_voltage = self.VE.list_expander(self.VE.random_voltage_list(230, 5))
        self.generator_list = [CustomGenerator(f"{i} - {self.typename}:{self.name}", self.VE) for i in range(num_of_gen)]
        self.load_list = [CustomLoad(f"{i} - {self.typename}:{self.name}", self.VE) for i in range(num_of_load)]
        self.total_mass = sum(map(lambda x: x.mass,  (self.generator_list+self.load_list)))
        self.power_factor = self.VE.RE.randint(900,1100)*0.001

    def network_syntax(self):
        return {
            'Bus': {'class_name': self.typename, 
                    'name': self.name},
            'Generators': [
                dict(gen.network_syntax(), **{'bus': self.name}) for gen in self.generator_list
            ],
            'Loads': [
                dict(load.network_syntax(), **{'bus': self.name}) for load in self.load_list
            ]
        }
    
    def average_efficiency(self):
        total_gen = len(self.generator_list)
        all_efficiency_list = list(map(lambda x: x.efficiency, self.generator_list))
        return list(map(lambda x: sum(x)/total_gen, zip(*all_efficiency_list)))
    
    def average_efficiency_index(self, index):
        return sum([eff for eff in map(lambda x: x.efficiency[index], self.generator_list)])/len(self.generator_list)
    
    def renew_voltage_list(self):
        new_voltage_list = self.VE.random_voltage_list(230, 5)
        new_voltage_list[0] = round(self.average_voltage[-1], 2)
        self.average_voltage = self.VE.list_expander(new_voltage_list)

    def renew(self):
        self.power_factor*=self.VE.RE.randint(900,1100)*0.001
        self.renew_voltage_list()
        for gen in self.generator_list:
            gen.renew_efficiency_list()

class CustomComponent:
    typename = None
    def __init__(self, name, valueEngine):
        self.VE = valueEngine
        self.name = name
        self.mass = self.VE.RE.randint(3, 5)
        self.power_list = self.VE.list_expander(self.VE.random_power_list())

    def network_syntax(self):
        return {
            'class_name': self.typename, 
            'name': self.name,
            'p_set': self.power_list
        }
    
    def renew_power_list(self):
        self.power_list = self.VE.list_expander(self.VE.random_power_list())

class CustomLoad(CustomComponent):
    typename = 'Load'
    def __init__(self, name, valueEngine):
        super().__init__(f"{self.typename}:{name}", valueEngine)

class CustomGenerator(CustomComponent):
    typename = 'Generator'
    def __init__(self, name, valueEngine):
        super().__init__(f"{self.typename}:{name}", valueEngine)
        self.efficiency = self.VE.list_expander(self.VE.random_efficiency_list())

    def renew_efficiency_list(self):
        new_efficiency_list = self.VE.random_efficiency_list()
        new_efficiency_list[0] = round(self.efficiency[-1], 2)
        self.efficiency = self.VE.list_expander(new_efficiency_list)