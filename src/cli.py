import argparse

import quantumexperiments.experimentlibrary as lib
from quantumexperiments.bell import BellExperiment
from quantumexperiments.coinflip import CoinFlipExperiment

experiments = {"bell": BellExperiment, "coin-flip": CoinFlipExperiment}


def main():
    args = get_args()
    experiment = experiments[args.experiment]()
    outcome = lib.perform(experiment, 1000)
    lib.print_outcome(outcome)


def get_args():
    parser = argparse.ArgumentParser(description="Run quantum computing experiments.")
    parser.add_argument("experiment", choices=experiments.keys())
    return parser.parse_args()
