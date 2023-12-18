from dataclasses import dataclass

from ._common import Aoc
from .tools.coordinates import Coordinate, Direction


@dataclass
class Beam:
    start: Coordinate
    length: int
    direction: Direction

    @property
    def coordinates(self) -> tuple[Coordinate, ...]:
        """All coordinates occupied by beam."""

        return tuple(self.start + (self.direction.value * i) for i in range(self.length + 1))


class Day16(Aoc):
    def part_1(self):
        with self.open_input() as file:
            mirrors_map = file.read()

            start = Coordinate(0, -1)

            beams = propagate_beam(start, Direction.RIGHT, mirrors_map, set())

            energized_tiles = set(coordinate for beam in beams for coordinate in beam.coordinates)
            energized_tiles.remove(start)

        return len(energized_tiles)

    def part_2(self) -> int:
        with self.open_input() as file:
            mirrors_map = file.read()

            all_energized_tiles = []

            vertical_len = len(mirrors_map.splitlines())
            horizontal_len = len(mirrors_map.splitlines()[0])

            right = [Coordinate(i, -1) for i in range(vertical_len)], Direction.RIGHT
            left = [Coordinate(i, horizontal_len) for i in range(vertical_len)], Direction.LEFT
            down = [Coordinate(-1, i) for i in range(horizontal_len)], Direction.DOWN
            up = [Coordinate(vertical_len, i) for i in range(horizontal_len)], Direction.UP

            for start, direction in [
                (coordinate, direction)
                for coordinates, direction in [right, left, down, up]
                for coordinate in iter(coordinates)
            ]:
                beams = propagate_beam(start, direction, mirrors_map, set())

                energized_tiles = set(coordinate for beam in beams for coordinate in beam.coordinates)
                energized_tiles.remove(start)

                all_energized_tiles.append(len(energized_tiles))

        return max(all_energized_tiles)


def propagate_beam(
    start: Coordinate, direction: Direction, mirrors_map: str, already_propagated: set[tuple[Coordinate, Direction]]
) -> list[Beam]:
    already_propagated.add((start, direction))

    map_rows = mirrors_map.splitlines()
    beams = []

    if direction.is_vertical():
        row = "".join([row[start.position] for row in map_rows])
        leftover = row[: start.row] if direction == direction.UP else row[start.row + 1 :]
    else:
        row = map_rows[start.row]
        leftover = row[: start.position] if direction == direction.LEFT else row[start.position + 1 :]

    if leftover:
        if direction in {Direction.UP, Direction.LEFT}:
            leftover = leftover[::-1]

        obstacles = leftover.replace(".", "")

        if obstacles:
            obstacle = obstacles[0]
            obstacle_diff = leftover.find(obstacle) + 1
            obstacle_coordinate = start + direction.value * obstacle_diff

            beam = Beam(start, obstacle_diff, direction)
            beams.append(beam)

            propagated = (
                propagate_beam(obstacle_coordinate, direction, mirrors_map, already_propagated)
                for direction in calculate_directions(direction, obstacle)
                if (obstacle_coordinate, direction) not in already_propagated
            )

            for propagate in propagated:
                beams.extend(propagate)

        else:
            beam = Beam(start, len(leftover), direction)
            beams.append(beam)

    return beams


def calculate_directions(beam_direction: Direction, obstacle: str) -> tuple[Direction]:
    match obstacle:
        case "|":
            new_directions = (
                (Direction.UP, Direction.DOWN)
                if beam_direction in {Direction.LEFT, Direction.RIGHT}
                else (beam_direction,)
            )
        case "-":
            new_directions = (
                (Direction.LEFT, Direction.RIGHT)
                if beam_direction in {Direction.UP, Direction.DOWN}
                else (beam_direction,)
            )
        case "/":
            new_directions = (
                beam_direction.rotate()
                if beam_direction in {Direction.UP, Direction.DOWN}
                else beam_direction.rotate(False),
            )
        case "\\":
            new_directions = (
                beam_direction.rotate(False)
                if beam_direction in {Direction.UP, Direction.DOWN}
                else beam_direction.rotate(),
            )
        case _:
            raise ValueError

    return new_directions
