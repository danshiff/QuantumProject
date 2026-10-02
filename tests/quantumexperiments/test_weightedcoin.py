import math
import unittest

from qiskit.quantum_info import Statevector

from quantumexperiments.weightedcoin import WeightedCoinFlipExperiment


class TestWeightedCoinFlip(unittest.TestCase):

    def test_probability_one_fifth(self):
        experiment = WeightedCoinFlipExperiment(1 / 5)

        state = Statevector.from_instruction(experiment.circuit)

        self.assertAlmostEqual(abs(state[0]), math.sqrt(4 / 5))
        self.assertAlmostEqual(abs(state[1]), math.sqrt(1 / 5))

    def test_probability_two_thirds(self):
        experiment = WeightedCoinFlipExperiment(2 / 3)

        state = Statevector.from_instruction(experiment.circuit)

        self.assertAlmostEqual(abs(state[0]), math.sqrt(1 / 3))
        self.assertAlmostEqual(abs(state[1]), math.sqrt(2 / 3))
