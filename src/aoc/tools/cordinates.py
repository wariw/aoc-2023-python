"""Helpers for cordinate based tasks."""

from dataclasses import dataclass
from enum import Enum
from typing import Self


@dataclass(frozen=True, eq=True)
class Cordinate:
    """Single cordinate."""

    row: int
    position: int

    def __add__(self, __value: Self) -> Self:
        return Cordinate(self.row + __value.row, self.position + __value.position)

    def __sub__(self, __value: Self) -> Self:
        return Cordinate(self.row - __value.row, self.position - __value.position)

    def __eq__(self, __value: Self) -> bool:
        return self.row == __value.row and self.position == __value.position


class Direction(Enum):
    """Direction diff values."""

    UP = Cordinate(-1, 0)
    DOWN = Cordinate(1, 0)
    LEFT = Cordinate(0, -1)
    RIGHT = Cordinate(0, 1)

    def is_horizontal(self) -> bool:
        return self in {self.LEFT, self.RIGHT}

    def is_vertical(self) -> bool:
        return not self.is_horizontal()


def get_adjacent_cordinates(cordinate: Cordinate, diagonal: bool = True) -> set[Cordinate]:
    """Returns cordinates adjacent to specified cordinate."""

    return set(
        Cordinate(cordinate.row + row, cordinate.position + position)
        for row in (-1, 0, 1)
        for position in (-1, 0, 1)
        if (row != 0 or position != 0)
        and ((row != position and abs(row - position) != 2) if not diagonal else True)
    )
