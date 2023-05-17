from sys import argv
from core import Core
from datetime import timedelta, datetime as dt
from time import sleep
from json import dumps
from libs.utils.data_functions import *
from libs.utils.adapter import BusAdapter

MODE = [
    'static',
    'stream'
]

def stream(core, bus_name, interval):
    while True:
        bus_object = core.bus_list[bus_name]
        _dict = {'bus': bus_name}
        
        datetime = dt.now()
        # datetime = dt(2023, 5, 13, 0, 0, 0)+timedelta(hours=i)
        now = str(datetime.replace(microsecond=0).time())

        if datetime.date() > dt.fromtimestamp(core.VE.TE.start_day).date():
            print("change")
            core.VE.TE.set_start_day(datetime.timestamp())
            bus_object.renew()

        core.network.lpf(now) # power calculation
        
        timeindex = int(dt.timestamp(datetime)-core.VE.TE.start_day) # voltage and efficiency calculation
        average_efficiency = bus_object.average_efficiency_index(timeindex)

        _dict['power'] = core.network.buses_t.p.loc[now][bus_name]*bus_object.power_factor
        _dict['voltage'] = bus_object.average_voltage[timeindex]
        _dict['temperature'] = bus_object.initial_temperature\
                               +_dict['power']*(1-average_efficiency)*core.VE.TE.resolution_by_seconds\
                                /(bus_object.total_mass*bus_object.heat_capacity)
        _dict['current'] = round(_dict['power']*average_efficiency/_dict['voltage'], 3)
        _dict['datetime'] = str(datetime)

        _json = dumps(_dict)
        print(_json)

        sleep(interval)

def static(core):
    core.network.lpf()

    import pandas as pd
    temp = {}
    voltage = {}
    current = {}
    index = core.network.buses_t.p.index.tolist()
    for bus in core.network.buses_t.p:
        current_bus = BusAdapter(core.network.buses_t.p[bus], core.bus_list[bus])
        temp[bus] = pd.Series(core.VE.calculate_temperature(current_bus), index=index)
        voltage[bus] = pd.Series(current_bus.v_set, index=index)
        current[bus] = pd.Series(core.VE.calculate_current(current_bus), index=index)

    core.network.buses_t['temp'] = pd.DataFrame(data=temp)
    core.network.buses_t['voltage'] = pd.DataFrame(data=voltage)
    core.network.buses_t['current'] = pd.DataFrame(data=current)

    df_plotter(core.network)
    df_combine = df_combiner(core.network)
    # cvs_converter(df_combine)
    grouped_csv_converter(df_combine, df_combine.Bus, '../output')

if __name__ == '__main__':
    assert len(argv) in (4, 5),\
    """
        Usage: python3 main.py static random_seed interval

        Usage: python3 main.py stream random_seed interval bus
    """
    assert argv[1] in MODE,\
    """
        Wrong mode
    """
    core = Core(argv[2], MODE.index(argv[1]), dt.now().timestamp(), int(argv[3]))
    if argv[1] == 'stream':
        assert len(argv) == 5,\
        """
            Missing parameter.
            Usage: python3 main.py stream random_seed interval bus
        """
        assert argv[4] in core.bus_list.keys(),\
        """
            No such bus in network. Check core.py again.
        """
        stream(core, argv[4], int(argv[3]))
    elif argv[1] == 'static':
        static(core)