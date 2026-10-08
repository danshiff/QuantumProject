import unittest
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


class TestMain(unittest.TestCase):
    @patch("cli.lib.print_outcome")
    @patch("cli.lib.perform")
    @patch("cli.get_args")
    def test_runs_bell_experiment(
        self,
        mock_get_args,
        mock_perform,
        mock_print_outcome,
    ):
        mock_get_args.return_value.experiment = "bell"
        mock_perform.return_value = {"00": 500, "11": 500}

        main()

        mock_perform.assert_called_once()
        experiment = mock_perform.call_args.args[0]

        self.assertIsInstance(experiment, BellExperiment)
        self.assertEqual(mock_perform.call_args.args[1], 1000)

        mock_print_outcome.assert_called_once_with({"00": 500, "11": 500})

    @patch("cli.lib.print_outcome")
    @patch("cli.lib.perform")
    @patch("cli.get_args")
    def test_runs_coin_flip_experiment(
        self,
        mock_get_args,
        mock_perform,
        mock_print_outcome,
    ):
        mock_get_args.return_value.experiment = "coin-flip"
        mock_perform.return_value = {"0": 500, "1": 500}

        main()

        mock_perform.assert_called_once()
        experiment = mock_perform.call_args.args[0]

        self.assertIsInstance(experiment, CoinFlipExperiment)
        self.assertEqual(mock_perform.call_args.args[1], 1000)

        mock_print_outcome.assert_called_once_with({"0": 500, "1": 500})
