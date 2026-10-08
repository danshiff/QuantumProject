import math

from qiskit import QuantumCircuit


class Grover:
    def __init__(self, target):
        self.target = str(target)
        for ch in str(self.target):
            if ch not in "01":
                raise ValueError("Target must be binary string")
        self.circuit = QuantumCircuit(len(self.target))
        self.initialize()
        times = self.find_optimal_times()
        self.grover(times)

    def initialize(self):
        for qubit in range(len(self.target)):
            self.circuit.h(qubit)

    def find_optimal_times(self):
        n = len(self.target)
        N = 2 ** n

        return round(math.pi / 4 * math.sqrt(N) - 0.5)

    def grover(self, times):
        for _ in range(times):
            self.oracle()
            self.diffuse()

    def oracle(self):
        self.map_to_all_1s()
        self.mark_all_1s()
        self.unmap()

    def map_to_all_1s(self):
        for ii, bit in enumerate(reversed(self.target)):
            if bit == "0":
                self.circuit.x(ii)


    def mark_all_1s(self):
        last_index = len(self.target) - 1
        self.circuit.h(last_index)
        self.circuit.mcx(list(range(last_index)), last_index)
        self.circuit.h(last_index)

    def unmap(self):
        self.map_to_all_1s() # It's a neat trick that the map undoes itself

    def diffuse(self):
        self.h_all()
        self.x_all()
        self.mark_all_1s()
        self.x_all()
        self.h_all()

    def h_all(self):
        for ii in range(len(self.target)):
            self.circuit.h(ii)

    def x_all(self):
        for ii in range(len(self.target)):
            self.circuit.x(ii)
