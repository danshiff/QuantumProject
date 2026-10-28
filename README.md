# Quantum Experiments

A Python project for exploring quantum computing concepts using
[Qiskit](https://qiskit.org/). Includes simple quantum experiments and implementations
of quantum algorithms, accessible through a command-line interface.

## Requirements

- Python 3.14.5 or later
- [uv](https://docs.astral.sh/uv/) for dependency management

## Installation

Clone the repository and install the project dependencies:

```bash
git clone https://github.com/danshiff/QuantumProject.git
cd quantumexperiments
uv sync
```

Run the CLI using `uv run`:

```bash
uv run quantum-experiments --help
```

## Usage

The CLI supports four experiments.

### Coin flip

Simulate a quantum coin flip using a Hadamard gate.

```bash
uv run quantum-experiments coin-flip
```

### Bell state

Prepare and measure a Bell state, demonstrating entanglement.

```bash
uv run quantum-experiments bell
```

### Weighted coin flip

Simulate a quantum coin with a specified probability of measuring `1`. The weight must
be between `0` and `1`, inclusive.

```bash
uv run quantum-experiments weighted-coin --weight 0.2
```

### Grover's algorithm

Run Grover's search algorithm with a binary string identifying the target state.

```bash
uv run quantum-experiments grover --target 1011
```

The target must be a nonempty binary string containing only `0` and `1`.

### Common options

All experiments accept the `--trials` option to specify the number of measurement
trials. The default is `1000`.

```bash
uv run quantum-experiments coin-flip --trials 10000
```

Use `--help` to see the available experiments and options:

```bash
uv run quantum-experiments --help
```

## Development

Dependencies are managed with `uv`. Install the project and its development
dependencies with:

```bash
uv sync
```

Run the test suite:

```bash
uv run pytest
```

Check code quality with Ruff:

```bash
uv run ruff check .
```

Check formatting:

```bash
uv run ruff format --check .
```
