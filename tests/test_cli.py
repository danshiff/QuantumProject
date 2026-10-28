import unittest
from argparse import Namespace
from unittest.mock import patch

from cli import get_args, main
from quantumexperiments.bell import BellExperiment
from quantumexperiments.coinflip import CoinFlipExperiment
from quantumexperiments.grover import Grover
from quantumexperiments.weightedcoin import WeightedCoinFlipExperiment


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

    def test_gets_weight(self):
        with patch(
            "sys.argv",
            ["quantum-experiments", "weighted-coin", "--weight", ".2"],
        ):
            args = get_args()
            self.assertEqual(0.2, args.weight)

    def test_weight_can_be_0(self):
        with patch(
            "sys.argv",
            ["quantum-experiments", "weighted-coin", "--weight", "0"],
        ):
            args = get_args()
            self.assertEqual(0, args.weight)

    def test_weight_can_be_1(self):
        with patch(
            "sys.argv",
            ["quantum-experiments", "weighted-coin", "--weight", "1"],
        ):
            args = get_args()
            self.assertEqual(1, args.weight)

    def test_weight_does_not_allow_negative(self):
        with patch(
            "sys.argv",
            ["quantum-experiments", "weighted-coin", "--weight", "-0.1"],
        ):
            with self.assertRaises(SystemExit):
                get_args()

    def test_weight_does_not_allow_greater_than_one(self):
        with patch(
            "sys.argv",
            ["quantum-experiments", "weighted-coin", "--weight", "1.1"],
        ):
            with self.assertRaises(SystemExit):
                get_args()

    def test_weight_does_not_allow_string(self):
        with patch(
            "sys.argv",
            ["quantum-experiments", "weighted-coin", "--weight", "point five"],
        ):
            with self.assertRaises(SystemExit):
                get_args()

    def test_gets_target(self):
        with patch("sys.argv", ["quantum-experiments", "grover", "--target", "1011"]):
            args = get_args()
            self.assertEqual("1011", args.target)

    def test_target_does_not_allow_2(self):
        with patch("sys.argv", ["quantum-experiments", "grover", "--target", "1021"]):
            with self.assertRaises(SystemExit):
                get_args()

    def test_target_does_not_allow_empty(self):
        with patch("sys.argv", ["quantum-experiments", "grover", "--target", ""]):
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
        **kwargs,
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
                experiment=experiment_name, trials=trials, **kwargs
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

    def test_runs_grover_experiment(self):
        self.assert_experiment_runs(
            experiment_name="grover",
            experiment_class=Grover,
            outcome={"1011": 990, "1111": 5, "0000": 5},
            target="1011",
        )

    def test_runs_weighted_coin_flip_experiment(self):
        self.assert_experiment_runs(
            experiment_name="weighted-coin",
            experiment_class=WeightedCoinFlipExperiment,
            outcome={"0": 800, "1": 200},
            weight=0.2,
        )

    def test_rejects_basic_coin_flip_if_target_param_given(self):
        with self.assertRaises(SystemExit):
            self.assert_experiment_runs(outcome={"0": 500, "1": 500}, target="0101")

    def test_rejects_basic_coin_flip_if_weight_param_given(self):
        with self.assertRaises(SystemExit):
            self.assert_experiment_runs(outcome={"0": 500, "1": 500}, weight=0.2)

    def test_grover_invalid_without_target(self):
        with self.assertRaises(SystemExit):
            self.assert_experiment_runs(
                experiment_name="grover",
                experiment_class=Grover,
                outcome={"1011": 990, "1111": 5, "0000": 5},
            )

    def test_weighted_coin_invalid_without_weight(self):
        with self.assertRaises(SystemExit):
            self.assert_experiment_runs(
                experiment_name="weighted-coin",
                experiment_class=WeightedCoinFlipExperiment,
                outcome={"0": 500, "1": 500},
            )
