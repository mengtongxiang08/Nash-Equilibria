"""
Nash Equilibria through Simulation

The purpose of this code is to simulate the emergence of Nash equilibria strategy through repeated gameplay.

Angela Xiang
1/202/026
How to run in the command line
  python main.py games/pd.txt
  python main.py games/rps.txt
                       ^ change this with the name of the text file (ex. pd, rps, bots, sh)   

AI Usage: asked Google gemini "how to print objects and decimal values 3 places"

Sources: https://www.w3schools.com/python/python_string_formatting.asp
"""

import sys
from game_parser import parse_game_file
from simulation import run_sessions
from plotting_one_screen import (
    show_5_plots_two_choice_one_screen,
    show_5_plots_rps_one_screen,
)
def log_basic_info(filename, num_choices, title, choice_names):
    """
    Print  logging
    Args:
        filename: file we loaded
        num_choices: number of choices
        title: title of game
        choice_names: list of strategy names

    Returns:
        None
    """
    print("Game file:", filename)
    print("Game title:", title)
    print("Number of choices:", num_choices)
    print("Choice names:", choice_names)
    print("========================================")


def main():
    """
    Reads a filename from the command line, runs the simulation,
    prints final preferences, and shows popup with 5 charts.

    Args:
        None

    Returns:
        None
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <gamefile.txt>")
        return

    filename = sys.argv[1]

    num_choices, title, choice_names, payoff_matrix = parse_game_file(filename)
    log_basic_info(filename, num_choices, title, choice_names)

    players, matchup_counts = run_sessions(num_choices, payoff_matrix, sessions=50, num_players=10)

    print("\nFinal player strategy preferences:")
    if num_choices == 2:
        for p in players:
            p0, p1 = p.final_probs()
            print(f"{p.name}: {choice_names[0]}={p0:.3f}, {choice_names[1]}={p1:.3f}")

        show_5_plots_two_choice_one_screen(title, choice_names, players)

    elif num_choices == 3:
        for p in players:
            probs = p.probs
            print(f"{p.name}: " +
                  f"{choice_names[0]}={probs[0]:.3f}, " +
                  f"{choice_names[1]}={probs[1]:.3f}, " +
                  f"{choice_names[2]}={probs[2]:.3f}")
        show_5_plots_rps_one_screen(title, choice_names, players)

    else:
        print("only 2-choice games and 3-choice RPS.")


if __name__ == "__main__":
    main()
