from qiskit.primitives import StatevectorSampler


def perform(experiment, trials):
    experiment.circuit.measure_all()
    sampler = StatevectorSampler()
    result = sampler.run([experiment.circuit], shots=trials).result()
    return result


def get_iter(outcome):
    counts = outcome[0].data.meas.get_counts()
    return iter(counts)


def print_outcome(outcome):
    print(outcome[0].data.meas.get_counts())


def main():
    pass


if __name__ == "__main__":
    main()
