"""
Player class for repeated gameplay .

- preferences: list of probabilities for each choice (must sum to 1.0)
- num_games, total_score, average_score
- history: list of snapshots of preferences over time (for plotting)

using the hint in teh assignment 
preference_next = preference_now + (score_this_game - averageScore) / 100
Then clamp to [0, 1], then re-normalize so all preferences sum to 1.
"""

import random

def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


class Player:
    def __init__(self, name, num_choices):
        self.name = name
        self.num_choices = num_choices

        # 0.5,0.5 for 2 choices)
        self.preferences = [1.0 / num_choices for _ in range(num_choices)]

        self.num_games = 0
        self.total_score = 0.0
        self.average_score = 0.0

        self.history = []
        self._save_history()
        self.choice_counts = [0 for _ in range(num_choices)]

    def _save_history(self):
        self.history.append(self.preferences[:])

    def pick_choice(self):
        """
        Randomly pick a choice index using the current preference probabilities.
        """
        r = random.random()
        running = 0.0
        for i, p in enumerate(self.preferences):
            running += p
            if r <= running:
                self.choice_counts[i] += 1
                return i
        self.choice_counts[-1] += 1
        return self.num_choices - 1

    def update_after_game(self, chosen_index, score_this_game):
        """
        Update preferences based on the payoff from the game.

        1) Compare score_this_game to average_score (BEFORE adding this score)
        2) Update the preference of the chosen strategy
        3) Clamp it to [0,1]
        4) Re-normalize all preferences so they sum to 1
        5) Update num_games, total_score, average_score
        6) Save history snapshot
        """
        old_avg = self.average_score

        change = (score_this_game - old_avg) / 100.0
        new_pref = self.preferences[chosen_index] + change
        new_pref = clamp(new_pref, 0.0, 1.0)
        self.preferences[chosen_index] = new_pref

        total = sum(self.preferences)
        if total == 0:
            self.preferences = [1.0 / self.num_choices for _ in range(self.num_choices)]
        else:
            self.preferences = [p / total for p in self.preferences]

        self.num_games += 1
        self.total_score += score_this_game
        self.average_score = self.total_score / self.num_games

        self._save_history()

    def check_preferences_sum(self, tolerance=1e-6):
        return abs(sum(self.preferences) - 1.0) < tolerance
