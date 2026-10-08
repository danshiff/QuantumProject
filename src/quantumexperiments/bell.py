from qiskit import QuantumCircuit


class BellExperiment:
    def __init__(self):
        self.circuit = QuantumCircuit(2)
        self.prepare()

    def prepare(self):
        self.circuit.h(0)
        self.circuit.cx(0, 1)
