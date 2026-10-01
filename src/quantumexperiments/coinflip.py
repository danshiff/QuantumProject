from qiskit import QuantumCircuit

from . import experimentlibrary as lib


class CoinFlipExperiment:
    def __init__(self):
        self.circuit = QuantumCircuit(1)
        self.prepare()
    def prepare(self):
        self.circuit.h(0)


def main():
    experiment = CoinFlipExperiment()
    result = lib.perform(experiment, 1000)
    lib.print_outcome(result)

if __name__ == '__main__':
    main()
