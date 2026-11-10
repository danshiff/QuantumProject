from qiskit import QuantumCircuit


class BernsteinVazirani:
    def __init__(self, target):
        self.target = str(target)
        for ch in str(self.target):
            if ch not in "01":
                raise ValueError("Target must be binary string")
        self.circuit = QuantumCircuit(len(self.target) + 1)
        self.initialize()
        self.oracle()
        self.decode()

    def initialize(self):
        ancilla = -1
        self.circuit.x(ancilla)
        for qubit in range(self.circuit.num_qubits):
            self.circuit.h(qubit)

    def oracle(self):
        pass

    def decode(self):
        pass
