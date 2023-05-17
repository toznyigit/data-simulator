import pypsa
import logging
from libs.network.custom_components import *
from libs.utils.engines import *

logging.basicConfig(level=logging.ERROR)

class Core:
    def __init__(self, seed='', mode=0, start_day='2023-01-01 00:00:00', resolution_by_seconds=1, time_period_as_day=1):
        resolution_by_seconds = 1 if mode else resolution_by_seconds
        self.VE = ValueEngine(RandomEngine(seed), TimestampEngine(start_day, resolution_by_seconds, time_period_as_day))
        self.network = pypsa.Network()
        snapshots = self.VE.TE.generate_timepoints() if mode else self.VE.TE.generate_timeseries()
        self.network.set_snapshots(snapshots)

        self.bus_list = {
            "A" : CustomBus("A", self.VE, self.VE.RE.randint(1, 4), self.VE.RE.randint(0, 5)),
            "B" : CustomBus("B", self.VE, self.VE.RE.randint(1, 4), self.VE.RE.randint(0, 5)),
            "C" : CustomBus("C", self.VE, self.VE.RE.randint(1, 4), self.VE.RE.randint(0, 5)),
            "D" : CustomBus("D", self.VE, self.VE.RE.randint(1, 4), self.VE.RE.randint(0, 5)),
            "E" : CustomBus("E", self.VE, self.VE.RE.randint(1, 4), self.VE.RE.randint(0, 5)),
            "F" : CustomBus("F", self.VE, self.VE.RE.randint(1, 4), self.VE.RE.randint(0, 5))
        }

        for _, v in self.bus_list.items():
            network_dict = v.network_syntax()
            self.network.add(**network_dict['Bus'])
            for gen in network_dict['Generators']: self.network.add(**gen)
            for load in network_dict['Loads']: self.network.add(**load)

        self.network.add("Line", "Line A-B", bus0=self.bus_list["A"].name, bus1=self.bus_list["B"].name)
        self.network.add("Line", "Line A-C", bus0=self.bus_list["A"].name, bus1=self.bus_list["C"].name)
        self.network.add("Line", "Line B-D", bus0=self.bus_list["B"].name, bus1=self.bus_list["D"].name)
        self.network.add("Line", "Line B-E", bus0=self.bus_list["B"].name, bus1=self.bus_list["E"].name)
        self.network.add("Line", "Line E-F", bus0=self.bus_list["E"].name, bus1=self.bus_list["F"].name)
        self.network.add("Line", "Line F-C", bus0=self.bus_list["F"].name, bus1=self.bus_list["C"].name)