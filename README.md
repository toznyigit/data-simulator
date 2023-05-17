# data-simulator

##### Usage Static
```
python3 main.py static random_seed interval
```
`static`: Use mode.

`random_seed`: Seed of random engine. Same seed generates same values by random engine.

`interval`: Time period that generate values in given interval.

##### Usage Stream

```
python3 main.py stream random_seed interval bus

```
`stream`: Use mode.

`random_seed`: Seed of random engine. Same seed generates same values by random engine.

`interval`: Time period that generate values in given interval.

`bus`: The system calculates values for each time interval from target bus. The target bus should included in core.network. `bus` parameter represents name of bus that can be found in `bus_list` and `network.add('Bus', bus)`.
