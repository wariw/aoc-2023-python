import re
from itertools import combinations

from .tools.coordinates import Coordinate
from ._common import Aoc


class Day11(Aoc):
    def part_1(self):
        with self.open_input() as file:
            universe_map = file.read()

        galaxies = find_galaxies(universe_map)
        expanded_galaxies = expand_cordinates(galaxies, universe_map)

        pairs = set(combinations(expanded_galaxies, 2))

        total_length = sum(manhattan_distance(*pair) for pair in pairs)

        return total_length

    def part_2(self) -> int:
        with self.open_input() as file:
            universe_map = file.read()

        galaxies = find_galaxies(universe_map)
        expanded_galaxies = expand_cordinates(galaxies, universe_map, 1000000)

        pairs = set(combinations(expanded_galaxies, 2))

        total_length = sum(manhattan_distance(*pair) for pair in pairs)

        return total_length


def expand_cordinates(
    galaxies: list[Coordinate], universe_map: str, factor: int = 2
) -> list[Coordinate]:
    """Expands cordinates according to universe map and factor.

    Args:
        galaxies (list[Coordinate]): Cordinates of galaxies to be expanded.
        universe_map (str): Map of universe.
        factor (int, optional): Expansion factor. Defaults to 2.

    Returns:
        list[Cordinate]: Expanded galaxy cordinates.

    """
    expansion_rows = [
        index for index, row in enumerate(universe_map.splitlines()) if "#" not in row
    ]
    expansion_columns = [
        index
        for index, column in enumerate(zip(*universe_map.splitlines()))
        if "#" not in column
    ]

    expanded_galaxies = []
    for cordinate in galaxies:
        expanded_row_counts = len(
            [row for row in expansion_rows if row < cordinate.row]
        )
        expanded_col_counts = len(
            [col for col in expansion_columns if col < cordinate.position]
        )
        expansion = factor - 1

        cordinate = Coordinate(
            cordinate.position + expanded_col_counts * expansion,
            cordinate.row + expanded_row_counts * expansion,
        )
        expanded_galaxies.append(cordinate)

    return expanded_galaxies


def find_galaxies(universe_map: str) -> list[Coordinate]:
    """Find galaxies in universe map.

    Args:
        galaxy (str): Map of universe.

    Returns:
        list[Coordinate]: Galaxies.

    """
    cordinates = []

    for row, galaxy_row in enumerate(universe_map.splitlines()):
        matches = re.finditer(r"#", galaxy_row)

        for match in matches:
            cordinate = Coordinate(row, match.start())
            cordinates.append(cordinate)

    return cordinates


def manhattan_distance(start: Coordinate, finish: Coordinate) -> int:
    """Calculates manhattan distance between two cordinates.

    Args:
        start (Coordinate): Start cordinate.
        finish (Coordinate): Finish cordinate.

    Returns:
        int: Path length.

    """
    return abs(finish.row - start.row) + abs(finish.position - start.position)
