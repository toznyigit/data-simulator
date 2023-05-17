from functools import reduce

def df_combiner(network):
    import pandas as pd
    network.buses_t.temp.index.name='snapshot'
    network.buses_t.voltage.index.name='snapshot'
    network.buses_t.current.index.name='snapshot'

    df_power = network.buses_t.p.reset_index().melt(id_vars="snapshot", var_name="Bus", value_name="Power")
    df_temp = network.buses_t.temp.reset_index().melt(id_vars="snapshot", var_name="Bus", value_name="Temperature")
    df_voltage = network.buses_t.voltage.reset_index().melt(id_vars="snapshot", var_name="Bus", value_name="Voltage")
    df_current = network.buses_t.current.reset_index().melt(id_vars="snapshot", var_name="Bus", value_name="Current")

    df_combined = reduce(lambda  left,right: pd.merge(left,right,on=["snapshot", "Bus"],
                                            how='inner'), [df_power, df_temp, df_voltage, df_current])

    df_combined.columns = ["DateTime", "Bus", "Power", "Temperature", "Voltage", "Current"]
    df_combined = df_combined.set_index("DateTime")
    df_combined = df_combined.sort_index()
    return df_combined

def csv_converter(df, path='output.csv'):
    df.to_csv(path)

def grouped_csv_converter(df, df_group, path='output.csv'):
    grouped = df.groupby(df_group)
    _path = path.split('.csv')[0]
    for group in grouped.groups.keys():
        csv_converter(grouped.get_group(group), f'{_path}_{group.lower().replace(" ","_")}.csv')  

def df_plotter(network):
    from matplotlib import pyplot as plt
    network.buses_t.p.plot()
    network.buses_t.temp.plot()
    network.buses_t.voltage.plot()
    network.buses_t.current.plot()
    plt.show()