"""
Simulation logic:
- 10 players
- Round robin each session => 45 games per session
- Run many sessions (default 50 sessions => 2250 games)

"""

from player import Player

def play_one_game(playerA, playerB, payoff_matrix):
    """
    Plays one game between playerA (row player) and playerB (col player).

    Returns:
      (choiceA, choiceB, payoffA, payoffB)
    """
    choiceA = playerA.pick_choice()
    choiceB = playerB.pick_choice()

    payoffA, payoffB = payoff_matrix[choiceA][choiceB]

    # Update each player based on their own payoff
    playerA.update_after_game(choiceA, payoffA)
    playerB.update_after_game(choiceB, payoffB)

    return choiceA, choiceB, payoffA, payoffB


def run_round_robin(players, payoff_matrix):
    """
    Run one full round robin:
      P1 plays P2..P10, P2 plays P3..P10, etc.

    Returns a list of game results.
    """
    results = []
    n = len(players)
    for i in range(n):
        for j in range(i + 1, n):
            pA = players[i]
            pB = players[j]
            results.append(play_one_game(pA, pB, payoff_matrix))
    return results


def run_sessions(num_choices, payoff_matrix, num_players=10, sessions=50):
    """
    Create players and run multiple sessions.

    Returns:
      players (list[Player])
      all_session_results (list[list[game_result]])
    """
    players = [Player(f"P{i+1}", num_choices) for i in range(num_players)]
    all_session_results = []

    for s in range(1, sessions + 1):
        session_results = run_round_robin(players, payoff_matrix)
        all_session_results.append(session_results)
    return players, all_session_results
