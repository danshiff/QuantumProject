import argparse

import quantumexperiments.experimentlibrary as lib
from quantumexperiments.bell import BellExperiment
from quantumexperiments.coinflip import CoinFlipExperiment

experiments = {"bell": BellExperiment, "coin-flip": CoinFlipExperiment}


def main():
    args = get_args()
    experiment = experiments[args.experiment]()
    outcome = lib.perform(experiment, args.trials)
    lib.print_outcome(outcome)


def get_args():
    parser = argparse.ArgumentParser(description="Run quantum computing experiments.")
    parser.add_argument("experiment", choices=experiments.keys())
    parser.add_argument(
        "--trials",
        type=positive_int,
        default=1000,
        help="Number of trials to run (default: 1000).",
    )
    return parser.parse_args()


def positive_int(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid integer")
    if number <= 0:
        raise argparse.ArgumentTypeError(f"'{value}' is not a positive integer")
    return number
