"""
PlayerTwoChoice class (for games with exactly 2 choices)

Angela Xiang 
1/20/2026

player for 2-choice games.
Instead of storing [p0, p1], we store only p1.
Because p0 is always (1 - p1).

Sources + AI : none

"""

import random


def clamp(x, low, high):
    """
    Clamp a number so it stays between low and high.

    Args:
        x: the number we want to clamp
        low: the smallest allowed value
        high: the largest allowed value

    Returns:
        The clamped number.
    """
    if x < low:
        return low
    if x > high:
        return high
    return x


class PlayerTwoChoice:
    """
      - p1: probability of choosing choice #1 (index 1)
      - games_played, total_score, average_score
      - history_p1: list of p1 values over time (for plotting)

      - After each game, it compares the payoff from that game
        to its average score so far, and nudges p1 up or down.
    """

    def __init__(self, name, start_p1=0.5):
        """
        Create a new 2-choice player.

        Args:
            name: player's name
            start_p1: starting probability of choosing choice #1

        Returns:
            None
        """
        self.name = name
        self.p1 = start_p1
        self.decision_history = []

        self.games_played = 0
        self.total_score = 0.0
        self.average_score = 0.0
        self.history_p1 = [self.p1]

    def choose(self):
        """
        Choose a move using the current probability.

        Rule:
          - returns 1 with probability p1
          - returns 0 with probability (1 - p1)

        Args:
            None

        Returns:
            An int (0 or 1), representing which choice was picked.
        """
        r = random.random()
        if r < self.p1:
            return 1
        return 0

    def update_after_game(self, chosen_index, payoff, step_divisor=15.0, eps=0.001):
        """
        Update the player's probability after a game.

          - If payoff > average, increase probability of the choice we used.
          - If payoff < average, decrease probability of the choice we used.
          - If we chose choice 1, we do p1 += change
          - If we chose choice 0, we do p1 -= change

        Args:
            chosen_index: 0 or 1 (what we chose this game)
            payoff: the score we got in this game (an int)
            step_divisor: the bigger this is the slower the pplayer adapts
            eps: prevents p1 from becoming exactly 0 or 1 (avoids “stuck forever” and the player always just chooses that)

        Returns:
            None
        """
        old_avg = self.average_score

        change = (payoff - old_avg) / step_divisor

        if chosen_index == 1:
            self.p1 += change
        else:
            self.p1 -= change

        # Keep p1 inside a safe range
        #0.001 - 0. 99
        self.p1 = clamp(self.p1, eps, 1.0 - eps)

        # Update score stats
        self.games_played += 1
        self.total_score += payoff
        self.average_score = self.total_score / self.games_played
        self.history_p1.append(self.p1)

    def final_probs(self):
        """
        Get the final probabilities in normal form.

        Args:
            None

        Returns:
            A tuple (p0, p1).
        """
        return (1.0 - self.p1, self.p1)
