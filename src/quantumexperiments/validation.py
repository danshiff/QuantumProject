import argparse


def binary_string(value):
    string = str(value)
    for ch in string:
        if ch not in "01":
            raise argparse.ArgumentTypeError(f"'{value}' is not a valid binary string")
    if string == "":
        raise argparse.ArgumentTypeError("target may not be empty")
    return string


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
