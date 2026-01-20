"""
PlayerNChoice class (for games with 3+ choices, like Rock-Paper-Scissors)

Author: YOUR NAME
Date: mm/dd/yyyy

This file defines a simple player that stores a list of probabilities.

AI Usage: ...
Sources: ...
"""

import random


def clamp(x, low, high):
    """
    Clamp a number so it stays between low and high.

    Args:
        x: number
        low: min
        high: max

    Returns:
        clamped number
    """
    if x < low:
        return low
    if x > high:
        return high
    return x


class PlayerNChoice:
    """
    A player for games with N choices (RPS uses N=3).

    What it stores:
      - probs: list like [p0, p1, p2]
      - games_played, total_score, average_score
      - history_probs: list of snapshots of probs over time

    How it learns:
      - After each game, it adjusts the probability of the chosen move
        based on (payoff - average_score), then re-normalizes so probs sum to 1.
    """

    def __init__(self, name, num_choices):
        """
        Create a new N-choice player.

        Args:
            name: player name
            num_choices: how many choices (3 for RPS)

        Returns:
            None
        """
        self.name = name
        self.num_choices = num_choices
        self.probs = [1.0 / num_choices for _ in range(num_choices)] #equally as likely

        self.games_played = 0
        self.total_score = 0.0
        self.average_score = 0.0
        self.history_probs = [self.probs[:]]

    def choose(self):
        """
        Choose a move using the probability list.

        Args:
            None

        Returns:
            An int index from 0..num_choices-1
        """
        r = random.random()
        running = 0.0
        for i, p in enumerate(self.probs):
            running += p
            if r <= running:
                return i
        return self.num_choices - 1

    def update_after_game(self, chosen_index, payoff, step_divisor=40.0, eps=0.001):
        """
          1) compute change = (payoff - average_score)/step_divisor
         and then add change to the chosen probability
          then clamp probabilities to avoid exact 0 or 1
          re-normalize so they sum to 1
         update score stats
       and save history snapshot

        Args:
            chosen_index: which move we chose
            payoff: score for that move this game
            step_divisor: bigger = slower learning
            eps: avoids probabilities becoming exactly 0

        Returns:
            None
        """
        old_avg = self.average_score
        change = (payoff - old_avg) / step_divisor

        self.probs[chosen_index] += change
        for i in range(self.num_choices):
            self.probs[i] = clamp(self.probs[i], eps, 1.0)

        total = sum(self.probs)
        self.probs = [p / total for p in self.probs]
        self.games_played += 1
        self.total_score += payoff
        self.average_score = self.total_score / self.games_played
        self.history_probs.append(self.probs[:])
