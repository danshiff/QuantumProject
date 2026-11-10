import math
import unittest

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from quantumexperiments.bernsteinvazirani import BernsteinVazirani


class TestBernsteinVazirani(unittest.TestCase):
    def setUp(self):
        self.target_state = "1011"
        self.experiment = BernsteinVazirani(self.target_state)

    def test_target_converted_to_string(self):
        experiment = BernsteinVazirani(1011)
        expected = self.target_state
        self.assertEqual(expected, experiment.target)

    def test_value_error_if_target_not_binary(self):
        with self.assertRaises(ValueError):
            BernsteinVazirani("1002")

    def test_initialize(self):
        self.reset_experiment()
        self.experiment.initialize()
        number_of_qubits = len(self.target_state) + 1
        absolute_amplitude = 1.0 / math.sqrt(2**number_of_qubits)
        number_of_amplitudes_per_sign = 2 ** (number_of_qubits - 1)
        expected_amplitudes = ([absolute_amplitude] * number_of_amplitudes_per_sign) + (
            [-absolute_amplitude] * number_of_amplitudes_per_sign
        )
        expected_state = Statevector(expected_amplitudes)
        self.assertEqual(expected_state, self.state)

    @property
    def state(self):
        return Statevector.from_instruction(self.experiment.circuit)

    def reset_experiment(self, state=None):
        self.experiment.circuit = QuantumCircuit(self.experiment.circuit.num_qubits)
        if state is not None:
            self.experiment.circuit.initialize(state)
