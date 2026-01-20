"""
simulation functions.

"""

from player_two_choice import PlayerTwoChoice
from player_n_choice import PlayerNChoice

def play_one_game(playerA, playerB, payoff_matrix):
    """
    Play one game between two players and update them.

    - For 2-choice players, we log the probability before choosing,
      and the action they chose. so bubble size = action counts.

    Returns:
        (choiceA, choiceB, payoffA, payoffB)
    """

    # strategy before choosing
    if hasattr(playerA, "p1"):
        pA0 = 1.0 - playerA.p1
        pA1 = playerA.p1
    if hasattr(playerB, "p1"):
        pB0 = 1.0 - playerB.p1
        pB1 = playerB.p1

    choiceA = playerA.choose()
    choiceB = playerB.choose()

    # log what they did at that probability
    if hasattr(playerA, "decision_history"):
        playerA.decision_history.append((pA0, pA1, choiceA))
    if hasattr(playerB, "decision_history"):
        playerB.decision_history.append((pB0, pB1, choiceB))

    payoffA, payoffB = payoff_matrix[choiceA][choiceB]

    playerA.update_after_game(choiceA, payoffA)
    playerB.update_after_game(choiceB, payoffB)

    return (choiceA, choiceB, payoffA, payoffB)



def run_sessions(num_choices, payoff_matrix, sessions=50, num_players=10):
    """
    Run many sessions of a 10-player round robin.

    For each session:
      - every player plays every other player once


      - we count how many times each player cohose each strategy
        for each matchup (P1 vs P2, etc.)

    Args:
        num_choices: number of choices in the game (2 or 3 here)
        payoff_matrix: payoff matrix from file
        sessions: how many full round robin sessions (min 50 required)
        num_players: should be 10 per assignment

    Returns:
        players: list of Player objects
        matchup_counts: dict with action counts for each matchup (only for 2-choice games)
    """

    if num_choices == 2:
        players = [PlayerTwoChoice(f"P{i+1}", start_p1=0.5) for i in range(num_players)]
    else:
        players = [PlayerNChoice(f"P{i+1}", num_choices=num_choices) for i in range(num_players)]

    matchup_counts = {}
    if num_choices == 2:
        for i in range(num_players):
            for j in range(i + 1, num_players):
                matchup_counts[(i, j)] = {"A": [0, 0], "B": [0, 0]}

    for session_index in range(sessions):
        for i in range(num_players):
            for j in range(i + 1, num_players):
                choiceA, choiceB, payoffA, payoffB = play_one_game(
                    players[i], players[j], payoff_matrix
                )
                if num_choices == 2:
                    matchup_counts[(i, j)]["A"][choiceA] += 1
                    matchup_counts[(i, j)]["B"][choiceB] += 1

    return players, matchup_counts
