from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, eq=True)
class Cordinate:
    """Single cordinate."""

    row: int
    position: int

    def __add__(self, other: Self) -> Self:
        return Cordinate(self.row + other.row, self.position + other.position)

    def __sub__(self, other: Self) -> Self:
        return Cordinate(self.row - other.row, self.position - other.position)

    def __eq__(self, __value: Self) -> bool:
        return self.row == __value.row and self.position == __value.position


def get_adjacent_cordinates(
    cordinate: Cordinate, diagonal: bool = True
) -> set[Cordinate]:
    """Returns cordinates adjacent to specified cordinate."""

    return set(
        Cordinate(cordinate.row + row, cordinate.position + position)
        for row in (-1, 0, 1)
        for position in (-1, 0, 1)
        if (row != 0 or position != 0)
        and ((row != position and abs(row - position) != 2) if not diagonal else True)
    )
