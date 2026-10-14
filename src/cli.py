import argparse

import quantumexperiments.experimentlibrary as lib
import quantumexperiments.validation as validation
from quantumexperiments.experimentregistry import EXPERIMENTS


def main():
    args = get_args()
    experiment = create_experiment(args)
    outcome = lib.perform(experiment, args.trials)
    lib.print_outcome(outcome)


def get_args():
    parser = argparse.ArgumentParser(description="Run quantum computing experiments.")
    parser.add_argument("experiment", choices=EXPERIMENTS.keys())
    parser.add_argument(
        "--trials",
        type=validation.positive_int,
        default=1000,
        help="Number of trials to run (default: 1000).",
    )
    for parameter in get_parameter_definitions():
        parser.add_argument(
            f"--{parameter.name}",
            type=parameter.converter_type,
            help=parameter.help,
        )
    return parser.parse_args()


def get_parameter_definitions():
    # This will cause problems if multiple experiments use the same names for
    # parameters with different types. That's not a problem for now.
    parameters = {}
    for definition in EXPERIMENTS.values():
        for parameter in definition.parameters:
            parameters[parameter.name] = parameter
    return parameters.values()


def create_experiment(args):
    definition = EXPERIMENTS[args.experiment]
    parameters = get_experiment_parameters(args, definition)
    validate_parameters(args, definition)

    return definition.experiment_class(**parameters)


def get_experiment_parameters(args, definition):
    parameters = {}
    for parameter in definition.parameters:
        value = getattr(args, parameter.name, None)
        if value is not None:
            parameters[parameter.name] = value
    return parameters


def validate_parameters(args, definition):
    validate_required_parameters(args, definition)
    validate_unexpected_parameters(args, definition)


def validate_required_parameters(args, definition):
    for parameter in definition.parameters:
        value = getattr(args, parameter.name, None)
        if parameter.required and value is None:
            raise SystemExit(
                f"Error: --{parameter.name} is required for {args.experiment}"
            )


def validate_unexpected_parameters(args, definition):
    allowed_parameters = {parameter.name for parameter in definition.parameters}
    supplied_parameters = {
        parameter.name
        for parameter in get_parameter_definitions()
        if getattr(args, parameter.name, None) is not None
    }
    unexpected_parameters = supplied_parameters - allowed_parameters

    if unexpected_parameters:
        names = ", ".join(f"--{name}" for name in sorted(unexpected_parameters))
        raise SystemExit(f"Error: {names} not allowed for {args.experiment}")
