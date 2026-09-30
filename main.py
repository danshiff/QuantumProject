from bell import BellExperiment
from coinflip import CoinFlipExperiment
import experimentlibrary as lib


def main():
    experiment = CoinFlipExperiment()
    flips = lib.perform(experiment, 1)
    bit = next(lib.get_iter(flips))
    real_exp = CoinFlipExperiment() if int(bit) == 1 else BellExperiment()
    new_flips = lib.perform(real_exp, 1000)
    lib.print_outcome(new_flips)


if __name__ == "__main__":
    main()
