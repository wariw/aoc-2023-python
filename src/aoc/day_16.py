from dataclasses import dataclass
from enum import StrEnum

from ._common import Aoc
from .tools.cordinates import Cordinate, Direction


@dataclass
class Beam:
    start: Cordinate
    length: int
    direction: Direction

    @property
    def cordiantes(self) -> tuple[Cordinate, ...]:
        return tuple(self.start + (self.direction.value * index) for index in range(self.length + 1))


class Obstacle(StrEnum):
    LINE = "|"
    MINUS = "-"
    MIRROR_A = "/"
    MIRROR_B = "\\"


class Day16(Aoc):
    def part_1(self):
        with self.open_input() as file:
            mirrors_map = file.read()

            start = Cordinate(0, -1)

            propagated = set()
            beams = propagate_beam(start, Direction.RIGHT, mirrors_map, propagated)

            energized_tiles = set()
            for beam in beams:
                for tiles in beam.cordiantes:
                    energized_tiles.add(tiles)
            energized_tiles.remove(start)

        return len(energized_tiles)

    def part_2(self) -> int:
        with self.open_input() as file:
            mirrors_map = file.read()

            all_energized_tiles = []

            vertical_len = len(mirrors_map.splitlines())
            horizontal_len = len(mirrors_map.splitlines()[0])

            right = [Cordinate(i, -1) for i in range(vertical_len)], Direction.RIGHT
            left = [Cordinate(i, horizontal_len) for i in range(vertical_len)], Direction.LEFT
            down = [Cordinate(-1, i) for i in range(horizontal_len)], Direction.DOWN
            up = [Cordinate(vertical_len, i) for i in range(horizontal_len)], Direction.UP

            for starts, direction in [right, left, down, up]:
                for start in starts:
                    propagated = set()
                    beams = propagate_beam(start, direction, mirrors_map, propagated)

                    energized_tiles = set()
                    for beam in beams:
                        for tiles in beam.cordiantes:
                            energized_tiles.add(tiles)
                    energized_tiles.remove(start)

                    all_energized_tiles.append(len(energized_tiles))

        return max(all_energized_tiles)


def propagate_beam(
    start: Cordinate, direction: Direction, mirrors_map: str, already_propagated: set[tuple[Cordinate, Direction]]
) -> list[Beam]:
    already_propagated.add((start, direction))

    map_rows = mirrors_map.splitlines()
    beams = []

    if direction.is_vertical():
        row = "".join([row[start.position] for row in map_rows])
        leftover = row[: start.row] if direction == direction.UP else row[start.row + 1:]
    else:
        row = map_rows[start.row]
        leftover = row[: start.position] if direction == direction.LEFT else row[start.position + 1 :]

    if leftover:
        if direction in {Direction.UP, Direction.LEFT}:
            leftover = leftover[::-1]

        obstacles = leftover.replace(".", "")

        if obstacles:
            obstacle = obstacles[0]
            beams = []

            obstacle_index = leftover.find(obstacle)

            obstacle_diff = obstacle_index + 1

            obstacle_cordinate = start + direction.value * obstacle_diff
            beam = Beam(start, obstacle_diff, direction)
            beams.append(beam)

            new_directions = calculate_directions(direction, Obstacle(obstacle))
            propagated = (
                propagate_beam(obstacle_cordinate, direction, mirrors_map, already_propagated)
                for direction in new_directions
                if (obstacle_cordinate, direction) not in already_propagated
            )

            for propagatee in propagated:
                beams.extend(propagatee)

        else:
            beam = Beam(start, len(leftover), direction)
            beams.append(beam)

    return beams


def calculate_directions(beam_direction: Direction, obstacle: Obstacle) -> tuple[Direction]:
    match obstacle:
        case Obstacle.LINE:
            new_directions = (
                (Direction.UP, Direction.DOWN)
                if beam_direction in {Direction.LEFT, Direction.RIGHT}
                else (beam_direction,)
            )
        case Obstacle.MINUS:
            new_directions = (
                (Direction.LEFT, Direction.RIGHT)
                if beam_direction in {Direction.UP, Direction.DOWN}
                else (beam_direction,)
            )
        case Obstacle.MIRROR_A:
            new_directions = (
                beam_direction.rotate()
                if beam_direction in {Direction.UP, Direction.DOWN}
                else beam_direction.rotate(False),
            )
        case Obstacle.MIRROR_B:
            new_directions = (
                beam_direction.rotate(False)
                if beam_direction in {Direction.UP, Direction.DOWN}
                else beam_direction.rotate(),
            )
        case _:
            raise ValueError

    return new_directions
