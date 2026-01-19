"""
RPS plotting with python-ternary (2-simplex).
We plot points for each player as (pRock, pPaper, pScissors)
and expect clustering near (1/3, 1/3, 1/3).
"""

def plot_rps_ternary(title, choice_names, players, filename_out):
    try:
        import ternary
        import matplotlib.pyplot as plt
    except ImportError:
        print("python-ternary is not installed.")
        print("Install it with: pip install python-ternary")
        return

    all_points = []
    for p in players:
        for h in p.history:
            all_points.append((h[0], h[1], h[2]))

    scale = 100
    scaled_points = []
    for (a, b, c) in all_points:
        scaled_points.append((a * scale, b * scale, c * scale))

    fig, tax = ternary.figure(scale=scale)
    tax.set_title(title)
    tax.boundary(linewidth=1.5)
    tax.gridlines(multiple=10, color="grey")

    tax.left_axis_label(choice_names[1], offset=0.14)  
    tax.right_axis_label(choice_names[2], offset=0.14)
    tax.bottom_axis_label(choice_names[0], offset=0.10)

    tax.scatter(scaled_points, marker="o", alpha=0.25, s=8)

    tax.ticks(axis="lbr", multiple=10, linewidth=1)
    tax.clear_matplotlib_ticks()

    fig.savefig(filename_out, dpi=200, bbox_inches="tight")
