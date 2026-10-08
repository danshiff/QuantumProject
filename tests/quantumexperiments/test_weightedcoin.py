import math
import unittest

from qiskit.quantum_info import Statevector

from quantumexperiments.weightedcoin import WeightedCoinFlipExperiment


class TestWeightedCoinFlip(unittest.TestCase):
    def test_probability_one_fifth(self):
        experiment = WeightedCoinFlipExperiment(1 / 5)

        state = Statevector.from_instruction(experiment.circuit)

        self.assertAlmostEqual(abs(state["0"]), math.sqrt(4 / 5))
        self.assertAlmostEqual(abs(state["1"]), math.sqrt(1 / 5))

    def test_probability_two_thirds(self):
        experiment = WeightedCoinFlipExperiment(2 / 3)

        state = Statevector.from_instruction(experiment.circuit)

        self.assertAlmostEqual(abs(state["0"]), math.sqrt(1 / 3))
        self.assertAlmostEqual(abs(state["1"]), math.sqrt(2 / 3))

    def test_probability_zero(self):
        experiment = WeightedCoinFlipExperiment(0)

        state = Statevector.from_instruction(experiment.circuit)

        self.assertAlmostEqual(abs(state["0"]), 1)
        self.assertAlmostEqual(abs(state["1"]), 0)

    def test_probability_one(self):
        experiment = WeightedCoinFlipExperiment(1)

        state = Statevector.from_instruction(experiment.circuit)

        self.assertAlmostEqual(abs(state["0"]), 0)
        self.assertAlmostEqual(abs(state["1"]), 1)

    def test_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            WeightedCoinFlipExperiment(-1)

    def test_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            WeightedCoinFlipExperiment(2)
