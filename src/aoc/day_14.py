from collections import defaultdict
from enum import auto, Enum, StrEnum
from typing import cast, Hashable, Optional

from aoc.tools.coordinates import Direction
from ._common import Aoc


class Day14(Aoc):
    def part_1(self):
        with self.open_input() as file:
            platform = file.read()
            platform = tilt_platform(platform, Direction.UP)

        return calculate_load(platform)

    def part_2(self) -> int:
        with self.open_input() as file:
            platform = file.read()

            repetitions_finder = RepetitionFinder()
            iterations = 1000000000

            for _ in range(iterations):
                old_platform = str(platform)

                platform = _spin_cycle(platform)

                repetitions_finder.add_element(old_platform, platform)

                if repetitions_finder.repetition:
                    repetition_start, repetitions = repetitions_finder.repetition
                    final_pattern_index = (iterations - repetition_start - 1) % len(
                        repetitions
                    )
                    final_valley = repetitions[final_pattern_index]
                    final_valley = cast(str, final_valley)
                    platform = _spin_cycle(final_valley)
                    break

        return calculate_load(platform)


class Stone(StrEnum):
    """Type of stone."""

    ROUND = "O"
    SQUARE = "#"


class RepetitionFinder:
    """Searches for repeating patterns."""

    class _FinderState(Enum):
        INIT = auto()
        PATTERN = auto()
        FINISHED = auto()

    def __init__(self):
        self._graph: dict[Hashable, list[Hashable]] = defaultdict(list)
        self._state: RepetitionFinder._FinderState = RepetitionFinder._FinderState.INIT
        self._pattern_started = False
        """Indicates that repeating pattern started."""

    @property
    def repetition(self) -> Optional[tuple[int, list[Hashable]]]:
        """Repetition start and repeating pattern or `None` if no repetition was found."""

        if self._state is RepetitionFinder._FinderState.FINISHED:
            return (
                len(self._get_vertex_by_repetitions(1)),
                self._get_vertex_by_repetitions(3) + self._get_vertex_by_repetitions(2),
            )

        return None

    def add_element(self, vertex: Hashable, element: Hashable):
        """Adds hashable item to graph while looking for repetitions."""

        if self._state is RepetitionFinder._FinderState.FINISHED:
            raise RuntimeError("Patter detection already complete.")

        self._graph[vertex].append(element)

        twos = len(self._get_vertex_by_repetitions(2))
        threes = len(self._get_vertex_by_repetitions(3))

        if twos == 1 and not threes:
            # Pattern starts when vertex with more than one repetiton shows up
            self._pattern_started = True

        if twos and threes == 1:
            # Pattern ends when first vertex with three repetitions shows up
            self._state = RepetitionFinder._FinderState.FINISHED

    def _get_vertex_by_repetitions(self, repetitions: int) -> list[Hashable]:
        """Returns vertices with specified number of repetitions."""

        return [
            vertex
            for vertex, elements in self._graph.items()
            if len(elements) == repetitions
        ]


def tilt_platform(platform: str, direction: Direction) -> str:
    """Tilts platform in specified directions causing boulders (`O`) to roll.

    Args:
        platform (str): Platform to be tilted.
        direction (Direction): Tilting direction.

    Returns:
        str: Tilted platform.

    """
    rows = platform.splitlines()

    if direction.is_vertical():
        rows = ["".join(row) for row in zip(*rows)]

    tilted_rows = [
        Stone.SQUARE.join(
            "".join(
                sorted(
                    group, reverse=direction not in {Direction.RIGHT, Direction.DOWN}
                )
            )
            for group in row.split(Stone.SQUARE)
        )
        for row in rows
    ]  # Splits rows by # and sorts remaining characters to achieve tiling effect.

    if direction.is_vertical():
        tilted_rows = ["".join(row) for row in zip(*tilted_rows)]

    return "\n".join(tilted_rows)


def calculate_load(platform: str) -> int:
    """Calculates load on platform."""

    return sum(
        (index + 1) * row.count(Stone.ROUND)
        for index, row in enumerate(reversed(platform.splitlines()))
    )


def _spin_cycle(platform: str) -> str:
    for direction in (Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT):
        platform = tilt_platform(platform, direction)

    return platform
