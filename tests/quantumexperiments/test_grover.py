import math
import unittest

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from quantumexperiments.grover import Grover


class TestGrover(unittest.TestCase):

    def setUp(self):
        self.target_state = "1011"
        self.experiment = Grover(self.target_state)

    def test_find_number_of_times(self):
        expected_number_of_oracle_diffusion_loops = 3
        actual = self.experiment.find_optimal_times()
        self.assertEqual(expected_number_of_oracle_diffusion_loops, actual)

    def test_initialize_is_all_equal(self):
        self.reset_experiment()
        self.experiment.initialize()
        expected_coefficient = 1 / 4
        for amplitude in self.state:
            self.assertAlmostEqual(expected_coefficient, amplitude)

    def test_oracle_flips_sign_of_target_amplitude(self):
        arbitrary_state = self.build_arbitrary_state()
        self.reset_experiment(state=arbitrary_state)
        self.experiment.oracle()
        target_index = int(self.target_state, 2)
        expected_state = Statevector(arbitrary_state.data)
        expected_state.data[target_index] *= -1
        self.assertEqual(expected_state, self.state)

    def test_diffuse_inverts_amplitudes_about_mean(self):
        arbitrary_state = self.build_arbitrary_state()
        marked_index = 4
        arbitrary_state.data[marked_index] *= -1
        initial_mean = sum(arbitrary_state.data) / len(arbitrary_state)

        self.reset_experiment(state=arbitrary_state)
        self.experiment.diffuse()

        expected_state = Statevector([2 * initial_mean - amplitude for amplitude in arbitrary_state])
        # The diffusion method rotates the global phase by pi. Since the phase is arbitrary, using equiv avoids testing
        # an incidental degree of freedom.
        self.assertTrue(self.state.equiv(expected_state))

    def test_grover(self):
        expected_probability = 0.9613
        actual_probability = abs(self.state[self.target_state]) ** 2
        self.assertAlmostEqual(expected_probability, actual_probability, places=4)

    @property
    def state(self):
        return Statevector.from_instruction(self.experiment.circuit)

    def reset_experiment(self, state=None):
        self.experiment.circuit = QuantumCircuit(len(self.target_state))
        if state is not None:
            self.experiment.circuit.initialize(state)

    @staticmethod
    def build_arbitrary_state():
        coefficients = range(1, 17)
        normalization = math.sqrt(sum(x ** 2 for x in coefficients))
        return Statevector([x / normalization for x in coefficients])
