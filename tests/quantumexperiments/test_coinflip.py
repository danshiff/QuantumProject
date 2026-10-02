import unittest

from qiskit.quantum_info import Statevector

from quantumexperiments.coinflip import CoinFlipExperiment


class TestCoinFlip(unittest.TestCase):

    def test_prepares_equal_superposition(self):
        experiment = CoinFlipExperiment()

        state = Statevector.from_instruction(experiment.circuit)

        expected = 1 / 2**0.5
        self.assertAlmostEqual(abs(state[0]), expected)
        self.assertAlmostEqual(abs(state[1]), expected)
