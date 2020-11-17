# COVID-19 Vaccine Simulation

This is a simulation package written in Python 3 for understanding the upcoming vaccine adoption from the behavioural aspect.

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

After installing all essential packages, you will need to download all `.py` files in this repository.

## Usage

```bash
python3 main.py [(N) (T) (alpha) (beta) (gamma) (phi) (delta)] ...\n\
  [-m]  <modes_config>] [-f (filename)] [-verbose | --v] [run]
```

Example usage:
```bash
py main.py 10 3 0.8 0.3 0.5 0.1 0.005
```
By adding 'run' at the end, the simulation will run automatically.
```bash
py main.py 10 3 0.8 0.3 0.5 0.1 0.005 run
```

If you did not use `run` at the end, you will arrive to the interface. The program will ask your command prompt (capitals does not matter).

* LOOK - View partner network.
* MODE - Change mode settings.
* RUN/ START - Start the simulation.
* SETTING - Set simulation settings.
* OTHER SETTING - Set auxiliary simulation parameters.
* SUMMARY - Print the simulation parameters.
* QUIT/ Q - Quit the software.

### Mode
This simulation can be customised by setting different modes. You may set them via express mode or under `MODE` comand. This simulation offers the following modes:

* 01 Living in city/rural
* 02 Travelled back from overseas
* 04 Bounded rationality of vaccine
* 05 Edit contact network
* 07 Age distribution
* 08 Gender distribution
* 10 Type of vaccine
* 11 Stop transmissability/ reduce severity
* 12 Cost of vaccine
* 13 Accessibility to vaccine
* 14 Side effects of vaccine
* 20 Intimacy game
* 21 Local majority rule
* 22 Stubbon to take vaccine
* 23 Stubbon to against vaccine
* 24 Contrary to social groups
* 31 Medication incorporated
* 41 Moral hazard of social distancing
* 42 Moral hazard of treatment
* 51: Erdos-Renyi topology
* 52: Scale free network
* 53: Small world topology
* 54: Lattice network

_Note: Not all modes have been equipped. You will not see anything if you tried to set up those._

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/).

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
