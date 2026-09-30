import math
from qiskit import QuantumCircuit

import experimentlibrary as lib


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


def main():
    experiment = WeightedCoinFlipExperiment(1/5)
    result = lib.perform(experiment, 1000)
    lib.print_outcome(result)


if __name__ == '__main__':
    main()
