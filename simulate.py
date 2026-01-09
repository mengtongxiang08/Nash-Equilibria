import sys
import random
import matplotlib.pyplot as plt

def read_game_file(filename: str):
    """
    Reads a game file and returns:
    - number of choices
    - game title
    - strategy names
    - payoff matrix
    """
    lines = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            li = line.strip()
            if li and not li.startswith("#"):
                lines.append(li)
