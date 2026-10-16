"""Regression checks for the notebook's runnable teaching algorithms."""
import ast
import contextlib
import io
import json
from pathlib import Path
import unittest

import numpy as np


def code_cell(notebook, marker):
    """Return the source of the one code cell containing `marker`.

    Looked up by content, not position, so inserted markdown cells cannot break the tests.
    """
    matches = ["".join(cell["source"]) for cell in notebook["cells"]
               if cell["cell_type"] == "code" and marker in "".join(cell["source"])]
    assert len(matches) == 1, f"expected one code cell containing {marker!r}, found {len(matches)}"
    return matches[0]


def load_algorithms():
    notebook = json.loads((Path(__file__).resolve().parents[1] /
                           "notebooks/01_rl_recommender_codealong.ipynb").read_text())
    namespace = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for marker in ("import numpy as np", "def validate_world"):
            exec(code_cell(notebook, marker), namespace)
        for marker in ("def run_random", "def run_epsilon_greedy", "def run_contextual"):
            tree = ast.parse(code_cell(notebook, marker))
            tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                         or (isinstance(node, ast.Assign) and any(
                             isinstance(target, ast.Name) and target.id in
                             ("true_rates_by_type", "visitor_types")
                             for target in node.targets))]
            exec(compile(tree, "notebook", "exec"), namespace)
    return namespace


class NotebookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.algorithms = load_algorithms()

    def test_fourth_banner_is_available_and_learned(self):
        counts, estimates, history = self.algorithms["run_epsilon_greedy"](
            rates=[0, 0, 0, 1], n_visitors=1000)
        self.assertTrue(np.all(counts > 0))
        self.assertEqual(counts.sum(), 1000)
        self.assertEqual(estimates.argmax(), 3)
        self.assertGreater(history.mean(), 0.8)

    def test_seed_is_independent_of_other_experiments(self):
        run = self.algorithms["run_epsilon_greedy"]
        first = run(n_visitors=100, seed=7)
        self.algorithms["run_random"](seed=123)
        self.algorithms["run_contextual"](n_visitors=50, seed=123)
        for before, after in zip(first, run(n_visitors=100, seed=7)):
            np.testing.assert_array_equal(before, after)

    def test_all_zero_ties_do_not_favor_first_banner(self):
        counts, _, _ = self.algorithms["run_epsilon_greedy"](
            n_visitors=1000, epsilon=0, rates=[0, 0, 0])
        self.assertTrue(np.all(counts > 200))

    def test_full_exploration_does_not_exploit_known_winner(self):
        counts, _, history = self.algorithms["run_epsilon_greedy"](
            n_visitors=6000, epsilon=1, rates=[0, 1, 0])
        self.assertTrue(np.all((counts > 1700) & (counts < 2300)))
        self.assertLess(history.mean(), 0.4)

    def test_invalid_inputs_fail_clearly(self):
        for args in ({"rates": []}, {"rates": [float("nan")]},
                     {"rates": [1.1]}, {"rates": [[0.1]]},
                     {"epsilon": -0.1}, {"n_visitors": 0}):
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.algorithms["run_epsilon_greedy"](**args)

    def test_short_horizon_and_single_action(self):
        for rates in ([0.2], [0.1, 0.2, 0.3, 0.4]):
            counts, _, history = self.algorithms["run_epsilon_greedy"](
                rates=rates, n_visitors=1)
            self.assertEqual(counts.sum(), 1)
            self.assertEqual(len(history), 1)


if __name__ == "__main__":
    unittest.main()
