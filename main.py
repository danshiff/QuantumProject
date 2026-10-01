from quantumexperiments.bell import BellExperiment
from quantumexperiments.coinflip import CoinFlipExperiment
from quantumexperiments import experimentlibrary as lib


def main():
    experiment = CoinFlipExperiment()
    flips = lib.perform(experiment, 1)
    bit = next(lib.get_iter(flips))
    real_exp = CoinFlipExperiment() if int(bit) == 1 else BellExperiment()
    new_flips = lib.perform(real_exp, 1000)
    lib.print_outcome(new_flips)


if __name__ == "__main__":
    main()
