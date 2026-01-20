"""
Game file parser for Nash Equilibria Simulation project.

Angela Xiang
1/20/2026

- Ignore blank lines and lines starting with '#'
- First real line: number of choices (int)
- Second real line: title (string)
- Next lines: a row label followed by payoff numbers

AI: asked Google GEmini "how to parse a python txt. file"
Sources: https://www.w3schools.com/python/python_file_open.asp, https://hackernoon.com/how-to-read-text-file-in-python
"""

def _useful_lines(filename):
    with open(filename, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line == "":
                continue
            if line.startswith("#"):
                continue
            yield line


def parse_game_file(filename):
    """
    Parse the game file and return:
      num_choices (int)
      title (str)
      choice_names (list[str])
      payoff_matrix (list[list[tuple(int,int)]])

    payoff_matrix[r][c] = (payoff_for_row_player, payoff_for_col_player)
    """
    lines = list(_useful_lines(filename))
    num_choices = int(lines[0])

    title = lines[1]

    row_lines = lines[2:]

    choice_names = []
    payoff_matrix = []

    for r in range(num_choices):
        parts = row_lines[r].split()
        if len(parts) < 1:
            raise ValueError("Bad row line (empty).")

        row_label = parts[0]
        nums = parts[1:]
        needed = num_choices * 2
        if len(nums) != needed:
            raise ValueError(
                f"Row '{row_label}' should have {needed} payoff numbers "
                f"(got {len(nums)}). Line was: {row_lines[r]}"
            )
        nums = [int(x) for x in nums]

        choice_names.append(row_label)

        row_payoffs = []
        idx = 0
        for c in range(num_choices):
            row_pay = nums[idx]
            col_pay = nums[idx + 1]
            row_payoffs.append((row_pay, col_pay))
            idx += 2

        payoff_matrix.append(row_payoffs)

    return num_choices, title, choice_names, payoff_matrix
