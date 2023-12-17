from pytest import mark

from aoc.tools.coordinates import Direction


@mark.parametrize("direction,opposite", (
        (Direction.UP, Direction.DOWN),
        (Direction.DOWN, Direction.UP),
        (Direction.LEFT, Direction.RIGHT),
        (Direction.RIGHT, Direction.LEFT)
))
def test_opposite(direction, opposite):
    assert direction.opposite == opposite


@mark.parametrize("direction,rotated", (
        (Direction.UP, Direction.RIGHT),
        (Direction.DOWN, Direction.LEFT),
        (Direction.LEFT, Direction.UP),
        (Direction.RIGHT, Direction.DOWN)
))
def test_rotate(direction, rotated):
    assert direction.rotate() == rotated
