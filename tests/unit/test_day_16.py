from pytest import mark

from aoc.day_16 import calculate_directions, Obstacle
from aoc.tools.coordinates import Direction

@mark.parametrize(
    "beam_direction, obstacle, new_direction",
    (
        # |
        (Direction.UP, Obstacle.LINE, (Direction.UP, )),
        (Direction.RIGHT, Obstacle.LINE, (Direction.UP, Direction.DOWN)),
        (Direction.LEFT, Obstacle.LINE, (Direction.UP, Direction.DOWN)),
        (Direction.DOWN, Obstacle.LINE, (Direction.DOWN, )),
        # -
        (Direction.UP, Obstacle.MINUS, (Direction.LEFT, Direction.RIGHT)),
        (Direction.RIGHT, Obstacle.MINUS, (Direction.RIGHT, )),
        (Direction.LEFT, Obstacle.MINUS, (Direction.LEFT, )),
        (Direction.DOWN, Obstacle.MINUS, (Direction.LEFT, Direction.RIGHT)),
        # /
        (Direction.UP, Obstacle.MIRROR_A, (Direction.RIGHT,)),
        (Direction.RIGHT, Obstacle.MIRROR_A, (Direction.UP,)),
        (Direction.LEFT, Obstacle.MIRROR_A, (Direction.DOWN,)),
        (Direction.DOWN, Obstacle.MIRROR_A, (Direction.LEFT,)),
        # \
        (Direction.UP, Obstacle.MIRROR_B, (Direction.LEFT,)),
        (Direction.RIGHT, Obstacle.MIRROR_B, (Direction.DOWN,)),
        (Direction.LEFT, Obstacle.MIRROR_B, (Direction.UP,)),
        (Direction.DOWN, Obstacle.MIRROR_B, (Direction.RIGHT,)),
    ),
)
def test_calculate_directions(beam_direction, obstacle, new_direction):
    assert calculate_directions(beam_direction, obstacle) == new_direction
