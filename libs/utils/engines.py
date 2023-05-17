import random, math
from datetime import datetime as dt

class RandomEngine:

    def __init__(self, seed=''):
        self.random_engine = random
        if seed: self.random_engine.seed(seed)
        self.randint = self.random_engine.randint
        self.random = self.random_engine.random
        self.uniform = self.random_engine.uniform

class TimestampEngine:

    def __init__(self,
            start_day='2023-01-01 00:00:00', 
            resolution_by_seconds=1 , #seconds
            time_period_as_day=1, #days
                                    ):
        self.start_day = int(start_day) if type(start_day) in (float, int)\
                                   else int(dt.strptime(start_day, '%Y-%m-%d %H:%M:%S').timestamp())
        self.resolution_by_seconds = resolution_by_seconds
        self.time_period_as_day = time_period_as_day
        self.timestamp_per_day = int(86400/resolution_by_seconds)

    def generate_timeseries(self):
        timeseries = []
        for gen_ts in range(self.start_day, self.start_day+self.time_period_as_day*86400, self.resolution_by_seconds):
            datetime = dt.fromtimestamp(gen_ts)
            timeseries.append(str(datetime))

        return timeseries
    
    def generate_timepoints(self):
        timepoints = []
        for gen_ts in range(-7200, 79200, self.resolution_by_seconds):
            time = dt.strftime(dt.fromtimestamp(gen_ts), '%H:%M:%S')
            timepoints.append(time)

        return timepoints
    
    def set_start_day(self, start_day):
        self.start_day = int(start_day) if type(start_day) in (float, int)\
                                   else int(dt.strptime(start_day, '%Y-%m-%d %H:%M:%S').timestamp())
class ValueEngine:

    def __init__(self, RE=RandomEngine(), TE=TimestampEngine()):
        self.RE = RE
        self.TE = TE

    def list_weighter(self, _list: list, method='uniform'):
        tmp = []

        if method == 'uniform':
            for _ in range(self.TE.time_period_as_day):
                tmp.extend(
                    map(lambda x: x*round(self.RE.uniform(3, 7),3), _list)
                )
        elif method == 'sin':
            sin_mult = 0.8
            for _ in range(self.TE.time_period_as_day):
                tmp.extend(
                    map(lambda x: x*(1-sin_mult+sin_mult*math.sin(self.RE.random()*math.pi)), _list)
                )
        elif method == '':
            for _ in range(self.TE.time_period_as_day):
                tmp.extend(
                    map(lambda x: x, _list)
                )

        return tmp

    def list_expander(self, _list: list, new_len: int=0):
        if not new_len: new_len = self.TE.timestamp_per_day
        old_len = len(_list)
        assert new_len > old_len
        tmp, result = _list, []
        tmp.extend([tmp[0]])

        for i in range(old_len):
            result.extend(
                [round(tmp[i]+j*(tmp[i+1]-tmp[i])/new_len, 3)
                    for j in range(new_len)
                ]
            )

        return [result[i] for i in range(0, len(result), old_len)]
    
    def random_power_list(self):
        return [self.RE.randint(self.RE.randint(30,70), self.RE.randint(135,300)) for _ in range(self.RE.randint(7,17))]
    
    def random_voltage_list(self, main_voltage, regulation_range):
        return [self.RE.uniform(main_voltage+regulation_range,main_voltage-regulation_range) for _ in range(self.RE.randint(4,8))]
    
    def random_efficiency_list(self):
        return [self.RE.randint(45,78)*0.01 for _ in range(self.RE.randint(3,7))]
    
    def calculate_temperature(self, bus):
        temp = []

        for power, efficiency in zip(bus.p_set, bus.e_set):
            energy = power*(1-efficiency)*self.TE.resolution_by_seconds
            delta_T = energy/(bus.mass*bus.heat_capacity)
            temp.append(bus.temperature+delta_T)
        
        return temp
    
    def calculate_temperature_index(self, bus, index):
        pass

    def calculate_current(self, bus):
        current = []
        for power, efficiency, voltage in zip(bus.p_set, bus.e_set, bus.v_set):
            effective_power = power*efficiency
            current.append( round(effective_power/voltage, 3) )
        
        return current
    

    def calculate_current_index(self, bus, index):
        pass