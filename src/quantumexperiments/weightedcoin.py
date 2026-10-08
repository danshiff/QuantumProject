import math

from qiskit import QuantumCircuit


class WeightedCoinFlipExperiment:
    def __init__(self, weight):
        self.weight = weight
        self.validate_input()
        self.circuit = QuantumCircuit(1)
        self.prepare()

    def validate_input(self):
        too_low = self.weight < 0
        too_high = self.weight > 1
        if too_low or too_high:
            raise ValueError("Weight must be between 0 and 1")

    def prepare(self):
        theta = 2 * math.asin(math.sqrt(self.weight))
        self.circuit.ry(theta, 0)
