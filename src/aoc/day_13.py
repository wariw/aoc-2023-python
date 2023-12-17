from typing import Optional

from aoc.tools.coordinates import Coordinate

from ._common import Aoc


class Day13(Aoc):
    def part_1(self):
        with self.open_input() as file:
            valley_map = file.read()
            patterns = valley_map.split("\n\n")

            total = 0
            for pattern in patterns:
                horizontal, vertical = _find_all_reflections(pattern)

                total += sum(reflection + 1 for reflection in vertical) + sum(
                    (reflection + 1) * 100 for reflection in horizontal
                )

        return total

    def part_2(self) -> int:
        with self.open_input() as file:
            valley_map = file.read()
            patterns = valley_map.split("\n\n")

            total = 0
            for pattern in patterns:
                horizontal, vertical = _find_all_reflections(pattern)
                horizontal_2, vertical_2 = _find_all_reflections(pattern, True)

                horizontal_diffs = set(horizontal_2) - set(horizontal)
                vertical_diffs = set(vertical_2) - set(vertical)

                horizontal_sum = sum(
                    (reflection + 1) * 100 for reflection in horizontal_diffs
                )
                vertical_sum = sum(reflection + 1 for reflection in vertical_diffs)

                total += horizontal_sum + vertical_sum

        return total


def check_for_reflection(
    index: int, rows: list[str], fix_smudge: bool = False
) -> tuple[bool, Optional[Coordinate]]:
    """Checks if reflections occurs at given index.

    Args:
        index (int): Index of reflection
        rows (list[str]): Valley map.
        fix_smudge (bool, optional): Decides if smudged mirors should be fixed. Defaults to False.

    Returns:
        tuple[bool, Optional[Coordinate]]: Reflection status and cordinate of fixed mirror.

    """
    current_row = index
    reflection = False
    smudge_replaced = None  # Only one smudge can be fixed per map.

    for i in range(index + 1):
        try:
            this_row = rows[current_row - i]
            next_row = rows[current_row + i + 1]
        except IndexError:
            break  # In case of final rows.

        if this_row != next_row:
            if fix_smudge and not smudge_replaced:
                diff = [
                    index
                    for index, (a, b) in enumerate(zip(this_row, next_row))
                    if a != b
                ]
                if len(diff) == 1:
                    smudge_replaced = Coordinate(current_row - i, diff[0])
                    reflection = True
                    continue

            return False, None

        reflection = True

    return reflection, smudge_replaced if reflection else None


def find_reflections(
    rows: list[str], allow_smudges: bool = False
) -> tuple[list[int], list[str]]:
    reflections = []
    for index in range(len(rows)):
        reflection, smudge = check_for_reflection(index, rows, allow_smudges)
        if smudge and allow_smudges:
            allow_smudges = False
            rows[smudge.row] = (
                rows[smudge.row][: smudge.position]
                + ("." if rows[smudge.row][smudge.position] == "#" else "#")
                + rows[smudge.row][smudge.position + 1 :]
            )  # Replace smudged mirror in map.
        if reflection and not allow_smudges:
            reflections.append(index)

    return reflections, rows


def _find_all_reflections(
    pattern: str, allow_smudges: bool = False
) -> tuple[list[int], list[int]]:
    rows = pattern.splitlines()
    horizontal_reflections, rows = find_reflections(rows, allow_smudges)
    columns = list("".join(row) for row in zip(*rows))
    vertical_reflections, _ = find_reflections(columns, allow_smudges)

    return horizontal_reflections, vertical_reflections
