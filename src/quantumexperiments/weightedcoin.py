import math
from qiskit import QuantumCircuit


class WeightedCoinFlipExperiment:
    def __init__(self, weight):
        assert weight >= 0
        assert weight <= 1
        self.weight = weight
        self.circuit = QuantumCircuit(1)
        self.prepare()

    def prepare(self):
        theta = 2 * math.asin(math.sqrt(self.weight))
        self.circuit.ry(theta, 0)
