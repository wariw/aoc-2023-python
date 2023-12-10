from aoc.tools.cordinates import Cordinate, get_adjacent_cordinates


def test_get_adjacent_cordinates():
    cordinate = Cordinate(2, 2)

    adjacent = get_adjacent_cordinates(cordinate)

    assert adjacent == {
        Cordinate(1, 1),
        Cordinate(1, 2),
        Cordinate(1, 3),
        Cordinate(2, 1),
        Cordinate(2, 3),
        Cordinate(3, 1),
        Cordinate(3, 2),
        Cordinate(3, 3),
    }


def test_get_adjacent_cordinates_not_diagonal():
    cordinate = Cordinate(2, 2)

    adjacent = get_adjacent_cordinates(cordinate, diagonal=False)

    assert adjacent == {
        Cordinate(1, 2),
        Cordinate(2, 1),
        Cordinate(2, 3),
        Cordinate(3, 2),
    }
