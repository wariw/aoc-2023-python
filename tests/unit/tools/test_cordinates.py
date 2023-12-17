from aoc.tools.coordinates import Coordinate, get_adjacent_cordinates


def test_get_adjacent_cordinates():
    cordinate = Coordinate(2, 2)

    adjacent = get_adjacent_cordinates(cordinate)

    assert adjacent == {
        Coordinate(1, 1),
        Coordinate(1, 2),
        Coordinate(1, 3),
        Coordinate(2, 1),
        Coordinate(2, 3),
        Coordinate(3, 1),
        Coordinate(3, 2),
        Coordinate(3, 3),
    }


def test_get_adjacent_cordinates_not_diagonal():
    cordinate = Coordinate(2, 2)

    adjacent = get_adjacent_cordinates(cordinate, diagonal=False)

    assert adjacent == {
        Coordinate(1, 2),
        Coordinate(2, 1),
        Coordinate(2, 3),
        Coordinate(3, 2),
    }
