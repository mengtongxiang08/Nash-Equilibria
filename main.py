"""
Mod/Sim Fall 2025 Final Project: Nash Equilibria through Simulation
Author: Angela Xiang
Date: 1/10/2026

This program:
- Parses a game file (ignores comments)
- Runs repeated 10-player round robin sessions
- Updates preferences iteratively (not one-shot Nash solving)
- Produces plots (matplotlib, and ternary for RPS if installed)
"""

import sys

from game_parser import parse_game_file
from simulation import run_sessions
from plotting_2choice import make_5_plots_2choice
from plotting_rps import plot_rps_ternary


def print_basic_log(filename, num_choices, title, choice_names):
    """Clean logging required by assignment: show file + game info."""
    print("========================================")
    print("Game file:", filename)
    print("Game title:", title)
    print("Number of choices:", num_choices)
    print("Choice names:", choice_names)
    print("========================================")


def print_final_strategies(players, choice_names):
    """
    Print each player's final preferences.
    This is useful to see convergence.
    """
    print("\nFinal player strategy preferences:")
    for p in players:
        pref_strs = []
        for i, name in enumerate(choice_names):
            pref_strs.append(f"{name}={p.preferences[i]:.3f}")
        print(p.name + ": " + ", ".join(pref_strs))


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <gamefile.txt>")
        return

    filename = sys.argv[1]
    num_choices, title, choice_names, payoff_matrix = parse_game_file(filename)
    print_basic_log(filename, num_choices, title, choice_names)
    players, all_session_results = run_sessions(
        num_choices=num_choices,
        payoff_matrix=payoff_matrix,
        num_players=10,
        sessions=50
    )

    print_final_strategies(players, choice_names)
    if num_choices == 2:
        make_5_plots_2choice(title, choice_names, players, out_prefix="output")

    elif num_choices == 3:
        plot_rps_ternary(title, choice_names, players, filename_out="output_rps_ternary.png")

if __name__ == "__main__":
    main()
