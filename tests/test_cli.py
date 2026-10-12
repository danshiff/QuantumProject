import unittest
from argparse import Namespace
from unittest.mock import patch

from cli import get_args, main
from quantumexperiments.bell import BellExperiment
from quantumexperiments.coinflip import CoinFlipExperiment


class TestGetArgs(unittest.TestCase):
    def test_gets_experiment(self):
        with patch("sys.argv", ["quantum-experiments", "bell"]):
            args = get_args()
        self.assertEqual(args.experiment, "bell")

    def test_rejects_invalid_experiment(self):
        with patch("sys.argv", ["quantum-experiments", "invalid"]):
            with self.assertRaises(SystemExit):
                get_args()

    def test_gets_trials(self):
        with patch("sys.argv", ["quantum-experiments", "bell", "--trials", "123"]):
            args = get_args()
        self.assertEqual(args.trials, 123)

    def test_trials_defaults_to_1000(self):
        with patch("sys.argv", ["quantum-experiments", "bell"]):
            args = get_args()
        self.assertEqual(args.trials, 1000)

    def test_trials_does_not_allow_zero(self):
        with patch("sys.argv", ["quantum-experiments", "bell", "--trials", "0"]):
            with self.assertRaises(SystemExit):
                get_args()

    def test_trials_does_not_allow_negative(self):
        with patch("sys.argv", ["quantum-experiments", "bell", "--trials", "-1"]):
            with self.assertRaises(SystemExit):
                get_args()

    def test_trials_does_not_allow_float(self):
        with patch("sys.argv", ["quantum-experiments", "bell", "--trials", "1.5"]):
            with self.assertRaises(SystemExit):
                get_args()

    def test_trials_does_not_allow_words(self):
        with patch("sys.argv", ["quantum-experiments", "bell", "--trials", "ten"]):
            with self.assertRaises(SystemExit):
                get_args()


class TestMain(unittest.TestCase):
    def setUp(self):
        self.default_experiment_name = "coin-flip"
        self.default_experiment = CoinFlipExperiment
        self.default_experiment_trials = 1000

    def assert_experiment_runs(
        self,
        experiment_name=None,
        experiment_class=None,
        trials=None,
        outcome=None,
    ):
        experiment_name = experiment_name or self.default_experiment_name
        experiment_class = experiment_class or self.default_experiment
        trials = trials if trials is not None else self.default_experiment_trials
        with (
            patch("cli.get_args") as mock_get_args,
            patch("cli.lib.perform", return_value=outcome) as mock_perform,
            patch("cli.lib.print_outcome") as mock_print_outcome,
        ):
            mock_get_args.return_value = Namespace(
                experiment=experiment_name,
                trials=trials,
            )

            main()

            experiment = mock_perform.call_args.args[0]
            mock_perform.assert_called_once_with(experiment, trials)
            self.assertIsInstance(experiment, experiment_class)
            mock_print_outcome.assert_called_once_with(outcome)

    def test_runs_bell_experiment(self):
        self.assert_experiment_runs(
            experiment_name="bell",
            experiment_class=BellExperiment,
            outcome={"00": 500, "11": 500},
        )

    def test_runs_coin_flip_experiment(self):
        self.assert_experiment_runs(
            outcome={"0": 500, "1": 500},
        )

    def test_runs_coin_flip_experiment_with_trials(self):
        self.assert_experiment_runs(
            trials=10,
            outcome={"0": 5, "1": 5},
        )
