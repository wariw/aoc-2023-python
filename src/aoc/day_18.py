from itertools import accumulate
from typing import NamedTuple

from ._common import Aoc
from .tools.coordinates import Coordinate, Direction


class Day18(Aoc):
    def part_1(self):
        with self.open_input() as file:
            steps = [_parse_step(step) for step in file.read().splitlines()]

            vertices = list(
                accumulate(
                    steps,
                    lambda coordinate, step: coordinate + step.direction.value * step.length,
                    initial=Coordinate(0, 0),
                )
            )[1:]
            edges = sum([step.length for step in steps])

            area = calculate_area(vertices)
            inside = area - (edges / 2) + 1  # Pick's theorem

        return int(inside + edges)

    def part_2(self) -> int:
        with self.open_input() as file:
            steps = [_parse_step(step, True) for step in file.read().splitlines()]

            vertices = list(
                accumulate(
                    steps,
                    lambda coordinate, step: coordinate + step.direction.value * step.length,
                    initial=Coordinate(0, 0),
                )
            )[1:]
            edges = sum([step.length for step in steps])

            area = calculate_area(vertices)
            inside = area - (edges / 2) + 1  # Pick's theorem

        return int(inside + edges)


class Step(NamedTuple):
    direction: Direction
    length: int


def calculate_area(vertices: list[Coordinate]) -> int:
    """Calculates area using shoelace algorithm.

    Vertices must go in the same direction.

    """
    x, y = zip(*[(c.row, c.position) for c in vertices])

    return abs(sum(i * j for i, j in zip(x, y[1:] + y[:1])) - sum(i * j for i, j in zip(x[1:] + x[:1], y))) / 2


def _parse_direction(direction: str) -> Direction:
    match direction:
        case "R" | "0":
            return Direction.RIGHT
        case "L" | "2":
            return Direction.LEFT
        case "U" | "3":
            return Direction.UP
        case "D" | "1":
            return Direction.DOWN


def _parse_step(step_text: str, use_colors: bool = False) -> Step:
    direction, count, color = step_text.split()

    if use_colors:
        return Step(
            _parse_direction(color[-2]),
            int(color[2:-2], 16),
        )

    return Step(_parse_direction(direction), int(count))
