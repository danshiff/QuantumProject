import unittest

from qiskit.quantum_info import Statevector

from quantumexperiments.bell import BellExperiment


class TestBell(unittest.TestCase):

    def test_prepares_phi_plus_state(self):
        experiment = BellExperiment()

        state = Statevector.from_instruction(experiment.circuit)

        expected_possible = 1 / 2**0.5
        expected_impossible = 0
        self.assertAlmostEqual(abs(state["00"]), expected_possible)
        self.assertEqual(abs(state["01"]), expected_impossible)
        self.assertEqual(abs(state["10"]), expected_impossible)
        self.assertAlmostEqual(abs(state["11"]), expected_possible)
