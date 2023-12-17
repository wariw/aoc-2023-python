"""Helpers for cordinate based tasks."""

from dataclasses import dataclass
from enum import Enum
from functools import singledispatchmethod
from typing import Self


@dataclass(frozen=True)
class Cordinate:
    """Single cordinate."""

    row: int
    position: int

    def __add__(self, other: Self) -> Self:
        return Cordinate(self.row + other.row, self.position + other.position)

    def __eq__(self, other: Self) -> bool:
        return self.row == other.row and self.position == other.position

    @singledispatchmethod
    def __mul__(self, other) -> Self:
        raise TypeError("Not supported.")

    @__mul__.register
    def _(self, other: int) -> Self:
        return Cordinate(self.row * other, self.position * other)

    def __sub__(self, other: Self) -> Self:
        return Cordinate(self.row - other.row, self.position - other.position)


class Direction(Enum):
    """Direction diff values."""

    UP = Cordinate(-1, 0)
    DOWN = Cordinate(1, 0)
    LEFT = Cordinate(0, -1)
    RIGHT = Cordinate(0, 1)

    @property
    def opposite(self) -> Self:
        return Direction(self.value * -1)

    def is_horizontal(self) -> bool:
        return self in {self.LEFT, self.RIGHT}

    def is_vertical(self) -> bool:
        return not self.is_horizontal()

    def rotate(self, clockwise: bool = True):
        if clockwise:
            return Direction(Cordinate(self.value.position, self.value.row * -1))

        return Direction(Cordinate(self.value.position * -1, self.value.row))


def get_adjacent_cordinates(cordinate: Cordinate, diagonal: bool = True) -> set[Cordinate]:
    """Returns cordinates adjacent to specified cordinate."""

    return set(
        Cordinate(cordinate.row + row, cordinate.position + position)
        for row in (-1, 0, 1)
        for position in (-1, 0, 1)
        if (row != 0 or position != 0)
        and ((row != position and abs(row - position) != 2) if not diagonal else True)
    )
