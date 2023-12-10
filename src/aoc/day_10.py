import re
from enum import Enum
from typing import Optional

from ._common import Aoc
from .tools.cordinates import Cordinate, get_adjacent_cordinates


class Direction(Enum):
    UP = Cordinate(-1, 0)
    DOWN = Cordinate(1, 0)
    LEFT = Cordinate(0, -1)
    RIGHT = Cordinate(0, 1)


cordinates_map = {
    "-": {Direction.LEFT, Direction.RIGHT},
    "|": {Direction.UP, Direction.DOWN},
    "L": {Direction.UP, Direction.RIGHT},
    "J": {Direction.UP, Direction.LEFT},
    "7": {Direction.DOWN, Direction.LEFT},
    "F": {Direction.DOWN, Direction.RIGHT},
}

directions_map = {
    Direction.RIGHT: ("J", "7", "-"),
    Direction.LEFT: ("F", "L", "-"),
    Direction.UP: ("|",),
    Direction.DOWN: ("|",),
}


class Traveler:
    """Helper class for maze traversing."""

    def __init__(
        self, maze_map_rows: list[str], start: Cordinate, previous: Cordinate
    ) -> None:
        self._maze_map_rows = maze_map_rows
        self._current = start
        self._previous = previous
        self._steps = 0

    @property
    def position(self) -> Cordinate:
        """Current position."""

        return self._current

    @property
    def steps(self) -> int:
        """Number of steps since start."""

        return self._steps

    def move_next(self) -> None:
        """Moves to next position accoring to maze map."""

        current_symbol = self._maze_map_rows[self._current.row][self._current.position]

        possible_directions = list(cordinates_map[current_symbol])
        
        previous_direction = Direction(self._previous - self._current)
        possible_directions.remove(previous_direction)

        next_direction = possible_directions[0]

        self._previous = self._current
        self._current += next_direction.value
        self._steps += 1


def _find_start(maze_map_rows: list[str]) -> Cordinate:
    for row, line in enumerate(maze_map_rows):
        start = re.search(r"S", line)
        if start:
            start_cordinate = Cordinate(row, start.start())

            return start_cordinate

    raise ValueError("No start provided in input.")


def _find_starting_cordinates(
    maze_map_rows: list[str], start_cordinate: Cordinate, possible_paths: set[Cordinate]
) -> list[Cordinate]:
    starting_cordinates = []
    for possible_path in possible_paths:
        direction = Direction(possible_path - start_cordinate)

        if (
            maze_map_rows[possible_path.row][possible_path.position]
            in directions_map[direction]
        ):
            starting_cordinates.append(possible_path)

    return starting_cordinates


class Day10(Aoc):
    def part_1(self):
        with self.open_input() as file:
            maze_map_rows = file.read().splitlines()

            start_cordinate = _find_start(maze_map_rows)
            possible_paths = get_adjacent_cordinates(start_cordinate, diagonal=False)
            start_points = _find_starting_cordinates(
                maze_map_rows, start_cordinate, possible_paths
            )

            travelers = list(
                Traveler(maze_map_rows, star_point, start_cordinate)
                for star_point in start_points
            )

            while travelers[0].position != travelers[1].position:
                for traveler in travelers:
                    traveler.move_next()

            total_steps = travelers[0].steps + 1

        return total_steps

    def part_2(self) -> int:
        with self.open_input() as file:
            maze_map_rows = file.read().splitlines()

            start_cordinate = _find_start(maze_map_rows)
            possible_paths = get_adjacent_cordinates(start_cordinate, diagonal=False)
            start_points = _find_starting_cordinates(
                maze_map_rows, start_cordinate, possible_paths
            )

            start_directions = [
                Direction(start_cordinate - start_point) for start_point in start_points
            ]
            start_symbol = [
                symbol
                for symbol, directions in cordinates_map.items()
                if directions == set(start_directions)
            ][0]

            traveler = Traveler(maze_map_rows, start_points[0], start_cordinate)

            positions = {start_cordinate}
            while traveler.position != start_cordinate:
                positions.add(traveler.position)
                traveler.move_next()

            inside_objects = 0
            for row, line in enumerate(maze_map_rows):
                inside = False
                last_bend: Optional[Direction] = None
                line = line.replace("S", start_symbol)

                for position, char in enumerate(line):
                    current_cordinate = Cordinate(row, position)

                    if current_cordinate in positions:
                        match char:
                            case "|":
                                inside = not inside
                            case "F" | "L":
                                last_bend = (
                                    Direction.DOWN if char == "F" else Direction.UP
                                )
                            case "J" | "7":
                                current_bend = (
                                    Direction.DOWN if char == "7" else Direction.UP
                                )
                                if last_bend != current_bend:
                                    inside = not inside
                                last_bend = None
                    else:
                        if inside:
                            inside_objects += 1

        return inside_objects
