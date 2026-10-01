from qiskit import QuantumCircuit

from . import experimentlibrary as lib


class BellExperiment:
    def __init__(self):
        self.circuit = QuantumCircuit(2)
        self.prepare()
    def prepare(self):
        self.circuit.h(0)
        self.circuit.cx(0, 1)


def main():
    experiment = BellExperiment()
    result = lib.perform(experiment, 1000)
    lib.print_outcome(result)

if __name__ == '__main__':
    main()
