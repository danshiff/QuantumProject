import argparse

import quantumexperiments.experimentlibrary as lib
from quantumexperiments.bell import BellExperiment
from quantumexperiments.coinflip import CoinFlipExperiment
from quantumexperiments.weightedcoin import WeightedCoinFlipExperiment

experiments = {
    "bell": BellExperiment,
    "coin-flip": CoinFlipExperiment,
    "weighted-coin": WeightedCoinFlipExperiment,
}


def main():
    args = get_args()
    experiment = create_experiment(args)
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
    parser.add_argument(
        "--weight",
        type=unit_interval_float,
        help="Chance for the weighted coin to land on 1 (between 0 and 1 inclusive)",
    )
    return parser.parse_args()


def create_experiment(args):
    if args.experiment == "weighted-coin":
        if getattr(args, "weight", None) is None:
            raise SystemExit("Error: --weight is required for weighted-coin")
        return experiments[args.experiment](weight=args.weight)
    if getattr(args, "weight", None) is not None:
        raise SystemExit("Error: --weight is only allowed for weighted-coin")
    return experiments[args.experiment]()


def positive_int(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid integer")
    if number <= 0:
        raise argparse.ArgumentTypeError(f"'{value}' is not a positive integer")
    return number


def unit_interval_float(value):
    try:
        number = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid number")
    if not 0 <= number <= 1:
        raise argparse.ArgumentTypeError("Weight must be between 0 and 1, inclusive")
    return number
