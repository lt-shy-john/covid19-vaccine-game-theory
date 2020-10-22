# COVID-19 Vaccine Simulation

This is a simulation package written in Python for understanding the upcoming vaccine adoption from the behavioural aspect.

## Getting Started

You may need the following Python libraries
* `numpy`
* `networkx`
* `matplotlib`

These libraries are common external ones. In case you need to use
```bash
pip install numpy
```
```bash
pip install networkx
```
```bash
pip install matplotlib
```

## Usage

```bash
python3 main.py (N) (T) (alpha) (beta) (gamma) (phi) (delta) ...\n\
  [-m]  <modes_config>] [-f (filename)] [run]
```

Example usage:
```bash
py main.py 10 3 0.8 0.3 0.5 0.1 0.005
```
By adding 'run' at the end, the simulation will run automatically.
```bash
py main.py 10 3 0.8 0.3 0.5 0.1 0.005 run
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
license:cc-by-sa-4.0
This work is licensed under [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/).
