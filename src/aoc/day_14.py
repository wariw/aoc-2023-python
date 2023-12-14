from collections import defaultdict
from typing import Hashable, Optional

from aoc.tools.cordinates import Direction
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

            for index in range(iterations):
                old_platform = str(platform)

                platform = _spin_cycle(platform)

                repetitions_finder.add_hash(old_platform, platform)

                if repetitions_finder.repetition:
                    repetition_start, repetitions = repetitions_finder.repetition
                    final_pattern_index = (iterations - repetition_start - 1) % len(repetitions)
                    final_valley = repetitions[final_pattern_index]
                    platform = _spin_cycle(final_valley)
                    break

        return calculate_load(platform)


class RepetitionFinder:
    """Repeating patterns finder."""

    def __init__(self):
        self._hash_map: dict[Hashable, list[Hashable]] = defaultdict(list)
        self._repetition_map: list[Hashable] = []
        self._started = False
        """Indicates that repeating pattern started."""

    def add_hash(self, key: Hashable, value: Hashable):
        """Ads hashable item to hash map while looking for repetitions."""

        self._hash_map[key].append(value)

        twos = len(list(filter(lambda x: len(x) == 2, self._hash_map.values())))
        threes = len(list(filter(lambda x: len(x) == 3, self._hash_map.values())))

        if twos == 1 and not threes:
            self._started = True

        if twos and threes == 1:
            self._started = False

        if self._started:
            self._repetition_map.append(key)

    @property
    def repetition(self) -> Optional[tuple[int, list[Hashable]]]:
        """Repetition start and repeating pattern or `None` if no repetition was found."""

        if self._repetition_map and not self._started:
            return len(list(filter(lambda x: len(x) == 1, self._hash_map.values()))), self._repetition_map


def tilt_platform(platform: str, direction: Direction) -> str:
    """Tilts platform in specified directions causing boulders (`O`) to roll.

    Args:
        platform (str): Platform to be tilted.
        direction (Direction): Tilting direction.

    Returns:
        str: Tilted platform.

    """
    rows = platform.splitlines()
    chars = ["O", "."]

    if direction.is_vertical():
        rows = ["".join(row) for row in zip(*rows)]

    if direction in {Direction.RIGHT, Direction.DOWN}:
        chars.reverse()

    new_rows = []
    for row in rows:
        groups = row.split("#")
        new_row = "#".join(chars[0] * group.count(chars[0]) + chars[1] * group.count(chars[1]) for group in groups)
        new_rows.append(new_row)

    if direction.is_vertical():
        new_rows = ["".join(row) for row in zip(*new_rows)]

    return "\n".join(new_rows)


def calculate_load(platform: str):
    """Calculates load on platform."""

    lines = platform.splitlines()
    size = len(lines)

    return sum([(size - index) * row.count("O") for index, row in enumerate(lines)])


def _spin_cycle(platform: str) -> str:
    platform = tilt_platform(platform, Direction.UP)
    platform = tilt_platform(platform, Direction.LEFT)
    platform = tilt_platform(platform, Direction.DOWN)
    platform = tilt_platform(platform, Direction.RIGHT)

    return platform
