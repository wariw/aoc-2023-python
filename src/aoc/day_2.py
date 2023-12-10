from enum import Enum, auto

from ._common import Aoc


class Cube(Enum):
    """Type of cube."""

    RED = auto()
    GREEN = auto()
    BLUE = auto()


cubes_map = {
    "red": Cube.RED,
    "green": Cube.GREEN,
    "blue": Cube.BLUE,
}


def parse_game_data(game_data: str) -> list[dict[Cube, int]]:
    """Parsed data for single game."""

    games = []

    for subset in game_data.split(";"):
        set_data = {}

        for cube_data in subset.split(","):
            count_string, cube_name = cube_data.split()
            cube = cubes_map[cube_name]
            set_data[cube] = int(count_string)

        games.append(set_data)

    return games


def _parse_games(games_data: str) -> dict[int, list[dict[Cube, int]]]:
    games = {}
    for game_data in games_data.splitlines():
        game_id_string, game_data_string = game_data.split(":")
        game_id = game_id_string.split()[1]
        parsed_game_data = parse_game_data(game_data_string[1:])
        games[int(game_id)] = parsed_game_data

    return games


def maximum_cubes(game_data: list[dict[Cube, int]]) -> tuple[int, int, int]:
    """Calculates maximum possible cubes in given game data.

    Args:
        game_data (list[dict[Cube, int]]): List of game subsets.

    Returns:
        tuple[int, int, int]: Counts of red, green and blue cubes.

    """
    red_count = 0
    green_count = 0
    blue_count = 0

    for game_set in game_data:
        if Cube.RED in game_set:
            red_count = max([game_set[Cube.RED], red_count])
        if Cube.GREEN in game_set:
            green_count = max([game_set[Cube.GREEN], green_count])
        if Cube.BLUE in game_set:
            blue_count = max([game_set[Cube.BLUE], blue_count])

    return red_count, green_count, blue_count


class Day2(Aoc):
    def part_1(self) -> int:
        id_sum = 0
        with self.open_input() as file:
            content = file.read()
            games = _parse_games(content)

            possible_cubes = {
                Cube.RED: 12,
                Cube.GREEN: 13,
                Cube.BLUE: 14,
            }

            for index, game in games.items():
                red_count, green_count, blue_count = maximum_cubes(game)

                if (
                    red_count <= possible_cubes[Cube.RED]
                    and green_count <= possible_cubes[Cube.GREEN]
                    and blue_count <= possible_cubes[Cube.BLUE]
                ):
                    id_sum += index

        return id_sum

    def part_2(self) -> int:
        power_sum = 0
        with self.open_input() as file:
            content = file.read()
            games = _parse_games(content)

            for game in games.values():
                red_count, green_count, blue_count = maximum_cubes(game)
                power = red_count * green_count * blue_count
                power_sum += power

        return power_sum
