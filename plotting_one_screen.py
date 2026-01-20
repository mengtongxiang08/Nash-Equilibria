"""
Plotting class to generate all 5 charts on one screen (2x3 grid, last spot empty).

- For RPS: ternary scatter plots

Author: Angela Xiang
Date:1/20/2026

AI Use: Google AI gemini "how to create legend in mat plot lib and color in the dots different colors"
Sources: https://plotly.com/python/ternary-plots/
https://www.goldensoftware.com/101-guide-to-ternary-class-scatter-plots/
"""
from matplotlib.lines import Line2D

import matplotlib.pyplot as plt
def show_5_plots_two_choice_one_screen(title, choice_names, players, decimals=3, size_scale=80):
    """
    - Each dot is a strategy point (probabilities) like (p(choice0), p(choice1))
    - Bubble size = number of times the player play that strategy
      while they were at (almsot) that probability.

      If a player had p1=0.90 many times AND kept choosing choice1,
      you will see a big bubble near (0.10, 0.90).

    Args:
        title: game title
        choice_names: like ["quiet", "confess"]
        players: list of PlayerTwoChoice
        decimals: rounding for grouping points
        size_scale: controls bubble sizes

    Returns:
        None
    """

    def points_from_decisions(player):
        """
        Turn decision_history -> scatter points.
          - if chosen == 0, we add to the bubble at (p0,p1) for action 0
          - if chosen == 1, we add to the bubble at (p0,p1) for action 1
        """
        counts = {}  # key: (x, y) -> how many times they chose at this point

        for (p0, p1, chosen) in player.decision_history:
            x = round(p0, decimals)
            y = round(p1, decimals)

            key = (x, y) #count decision at x,y
            counts[key] = counts.get(key, 0) + 1

        xs, ys, sizes = [], [], []
        for (x, y), freq in counts.items():
            xs.append(x)
            ys.append(y)
            sizes.append(freq * size_scale)

        return xs, ys, sizes

    pairs = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]

    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    fig.suptitle(title + " (5 matchups)", fontsize=14)
    axes = axes.flatten()

    for k, (i, j) in enumerate(pairs):
        ax = axes[k]
        pA = players[i]
        pB = players[j]

        Axs, Ays, As = points_from_decisions(pA)
        Bxs, Bys, Bs = points_from_decisions(pB)

        ax.scatter(Axs, Ays, s=As, alpha=0.35, color="tab:blue")
        ax.scatter(Bxs, Bys, s=Bs, alpha=0.35, color="tab:orange")

        ax.set_title(f"{pA.name} vs {pB.name}", fontsize=10)
        ax.set_xlabel(choice_names[0], fontsize=9)
        ax.set_ylabel(choice_names[1], fontsize=9)

        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True)

        legend_handles = [
            Line2D([0], [0], marker='o', linestyle='', markersize=6,
                   label=pA.name, alpha=0.35, color="tab:blue"),
            Line2D([0], [0], marker='o', linestyle='', markersize=6,
                   label=pB.name, alpha=0.35, color="tab:orange"),
        ]
        ax.legend(handles=legend_handles, fontsize=8, loc="upper right")

    axes[5].axis("off")
    plt.tight_layout()
    plt.show()


def show_5_plots_rps_one_screen(title, choice_names, players, size_scale=8, scale=100):
    """
        pip install python-ternary

    Args:
        title: game title
        choice_names: like ["rock", "paper", "scissors"]
        players: list of PlayerNChoice (num_choices=3)
        size_scale: bubble size control
        scale: ternary triangle scale (100 is convenient)

    Returns:
        None
    """
    try:
        import ternary
        from matplotlib.lines import Line2D
    except ImportError:
        print("ERROR: python-ternary not installed.")
        print("Run: pip install python-ternary")
        return

    pairs = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]

    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    fig.suptitle(title + " (RPS, 5 matchups)", fontsize=14)
    axes = axes.flatten()

    # Legend handles
    legend_handles = [
        Line2D([0], [0], marker='o', linestyle='', markersize=6,
               label='Player A', alpha=0.30, color="tab:blue"),
        Line2D([0], [0], marker='o', linestyle='', markersize=6,
               label='Player B', alpha=0.40, color="tab:orange"),
    ]

    for k, (i, j) in enumerate(pairs):
        ax = axes[k]
        pA = players[i]
        pB = players[j]

        tax = ternary.TernaryAxesSubplot(ax=ax, scale=scale)
        tax.boundary(linewidth=1.0)
        tax.gridlines(multiple=20, linewidth=0.5)

        tax.left_axis_label(choice_names[1], fontsize=8, offset=0.12)
        tax.right_axis_label(choice_names[2], fontsize=8, offset=0.12)
        tax.bottom_axis_label(choice_names[0], fontsize=8, offset=0.06)

        def history_points(player):
            pts = []
            for probs in player.history_probs:
                a = probs[0] * scale
                b = probs[1] * scale
                c = probs[2] * scale
                pts.append((a, b, c))
            return pts

        ptsA = history_points(pA)
        ptsB = history_points(pB)

        tax.scatter(ptsA, alpha=0.30, s=size_scale, color="tab:blue")
        tax.scatter(ptsB, alpha=0.40, s=size_scale, color="tab:orange")

        ax.set_title(f"{pA.name} vs {pB.name}", fontsize=10)
        legend_handles = [
            Line2D([0], [0], marker='o', linestyle='', markersize=6,
                   label=pA.name, alpha=0.30, color="tab:blue"),
            Line2D([0], [0], marker='o', linestyle='', markersize=6,
                   label=pB.name, alpha=0.40, color="tab:orange"),
        ]
        ax.legend(handles=legend_handles, fontsize=8, loc="upper right")

        tax.clear_matplotlib_ticks()

    axes[5].axis("off")
    plt.tight_layout()
    plt.show()
