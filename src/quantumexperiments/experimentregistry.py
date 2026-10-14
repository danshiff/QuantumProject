from dataclasses import dataclass
from typing import Callable

import quantumexperiments.validation as validation
from quantumexperiments.bell import BellExperiment
from quantumexperiments.coinflip import CoinFlipExperiment
from quantumexperiments.weightedcoin import WeightedCoinFlipExperiment


@dataclass(frozen=True)
class ParameterDefinition:
    name: str
    converter_type: Callable[[str], object]
    required: bool = True
    help: str = ""


@dataclass(frozen=True)
class ExperimentDefinition:
    experiment_class: type
    parameters: tuple[ParameterDefinition, ...] = ()


EXPERIMENTS = {
    "bell": ExperimentDefinition(BellExperiment),
    "coin-flip": ExperimentDefinition(CoinFlipExperiment),
    "weighted-coin": ExperimentDefinition(
        WeightedCoinFlipExperiment,
        parameters=(
            ParameterDefinition(
                name="weight",
                converter_type=validation.unit_interval_float,
                help="Chance for the weighted coin to land on 1 (0 to 1 inclusive).",
            ),
        ),
    ),
}
