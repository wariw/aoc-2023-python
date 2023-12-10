from aoc.day_2 import Cube, parse_game_data


def test_parse_game_data():
    assert parse_game_data("3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == [
        {Cube.BLUE: 3, Cube.RED: 4},
        {Cube.RED: 1, Cube.GREEN: 2, Cube.BLUE: 6},
        {Cube.GREEN: 2},
    ]
