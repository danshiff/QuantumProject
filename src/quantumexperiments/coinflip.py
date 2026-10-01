from qiskit import QuantumCircuit


class CoinFlipExperiment:
    def __init__(self):
        self.circuit = QuantumCircuit(1)
        self.prepare()
    def prepare(self):
        self.circuit.h(0)
