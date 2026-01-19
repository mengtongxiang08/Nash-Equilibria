"""
5 plots for fixed matchups
(P1,P2), (P3,P4), (P5,P6), (P7,P8), (P9,P10)

Each plot shows BOTH players as points in (choice0_prob, choice1_prob).
Bubble size is based on how many times the player picked choice1 overall
"""

import matplotlib.pyplot as plt

def plot_pair_2choice(title, choice_names, playerA, playerB, filename_out):
    """
    Create a scatter plot showing preference history for two players.

    x = prob(choice 0)
    y = prob(choice 1)
    bubble size = times chose choice 1 so far (cumulative)
    """

    Ax = [h[0] for h in playerA.history]
    Ay = [h[1] for h in playerA.history]

    Bx = [h[0] for h in playerB.history]
    By = [h[1] for h in playerB.history]
    Asizes = [max(10, i) for i in range(len(playerA.history))]
    Bsizes = [max(10, i) for i in range(len(playerB.history))]

    plt.figure()
    plt.scatter(Ax, Ay, s=Asizes, alpha=0.35, label=playerA.name)
    plt.scatter(Bx, By, s=Bsizes, alpha=0.35, label=playerB.name)

    plt.title(title + f" ({playerA.name} vs {playerB.name})")
    plt.xlabel(choice_names[0] + " probability")
    plt.ylabel(choice_names[1] + " probability")
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.legend()
    plt.grid(True)

    plt.savefig(filename_out, dpi=200, bbox_inches="tight")
    plt.close()


def make_5_plots_2choice(title, choice_names, players, out_prefix):
    """
    Make 5 plots using the  pairings:
      (P1,P2), (P3,P4), (P5,P6), (P7,P8), (P9,P10)
    """
    pairs = [(0,1), (2,3), (4,5), (6,7), (8,9)]
    for k, (i, j) in enumerate(pairs, start=1):
        pA = players[i]
        pB = players[j]
        filename_out = f"{out_prefix}_plot{k}_{pA.name}_vs_{pB.name}.png"
        plot_pair_2choice(title, choice_names, pA, pB, filename_out)
