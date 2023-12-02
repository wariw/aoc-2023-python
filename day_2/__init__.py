import re

from enum import Enum, auto


class Cube(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


def parse_cube(cube_data: str) -> tuple[Cube, int]:
    count, cube = re.findall(r"(\d+) (red|green|blue)", cube_data)[0]

    match cube:
        case "red":
            cube_type = Cube.RED
        case "green":
            cube_type = Cube.GREEN
        case "blue":
            cube_type = Cube.BLUE

    return cube_type, int(count)


def parse_game(game_data: str) -> list[dict[Cube, int]]:
    games_data = game_data.split(";")
    game_list = []
    for game_data in games_data:
        cubes = game_data.split(",")
        set_data = {}
        for cube in cubes:
            cube_type, count = parse_cube(cube)
            set_data[cube_type] = count
        game_list.append(set_data)

    return game_list


def parse_games(games_data: str) -> dict[int, list[dict[Cube, int]]]:
    games_data = games_data.splitlines()
    games = {}
    for game_data in games_data:
        game_id, data = re.findall(r"Game (\d+): (.*)", game_data)[0]
        parsed_game_data = parse_game(data)
        games[int(game_id)] = parsed_game_data

    return games


def maximum_cubes(game_data: list[dict[Cube, int]]) -> dict[Cube, int]:
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


def part_1() -> int:
    id_sum = 0
    with open("day_2/input.txt", "rt") as file:
        content = file.read()
        games = parse_games(content)

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


def part_2() -> int:
    power_sum = 0
    with open("day_2/input.txt", "rt") as file:
        content = file.read()
        games = parse_games(content)

        for game in games.values():
            red_count, green_count, blue_count = maximum_cubes(game)
            power = red_count * green_count * blue_count
            power_sum += power


    return power_sum


if __name__ == "__main__":
    print(part_1())
    print(part_2())
