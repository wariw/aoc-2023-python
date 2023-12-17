import re
from dataclasses import dataclass

from ._common import Aoc
from .tools.coordinates import Coordinate, get_adjacent_cordinates


@dataclass(frozen=True, eq=True)
class CordinateObject:
    """Cordinated object."""

    value: str
    start: Coordinate
    span: int

    @property
    def indices(self) -> list[Coordinate]:
        """Indices occupied by object."""

        return [
            Coordinate(self.start.row, self.start.position + index)
            for index in range(self.span)
        ]


def parse_objects(parts_map: str) -> tuple[set[CordinateObject], set[CordinateObject]]:
    """Parses cordinate objects (numbers and symbols) from provided map.

    Args:
        parts_map (str): Multiline string providing cordinat map.

    Returns:
        tuple[set[CordinateObject], set[CordinateObject]]: Tuple containing sets of number na symbol cordinates.

    """
    map_rows = parts_map.splitlines()
    numbers = set()
    symbols = set()

    for row_index, map_row in enumerate(map_rows):
        for match in re.finditer(r"(?!\.)\W|\d+", map_row):
            cordinate = CordinateObject(
                match.group(),
                Coordinate(row_index, match.start()),
                match.end() - match.start(),
            )
            try:
                int(match.group())
                numbers.add(cordinate)
            except ValueError:
                symbols.add(cordinate)

    return numbers, symbols


class Day3(Aoc):
    def part_1(self) -> int:
        with self.open_input() as file:
            content = file.read()
            numbers, symbols = parse_objects(content)

            symbol_cordinates = set(
                cordinates
                for symbol in symbols
                for cordinates in get_adjacent_cordinates(symbol.start)
            )  # Get cordinates adjacent to symbols

            part_numbers = set(
                number
                for number in numbers
                for cordinate in number.indices
                if cordinate in symbol_cordinates
            )  # Select numbers adjacent to symbols

            part_numbers_sum = sum(int(part.value) for part in part_numbers)

            return part_numbers_sum

    def part_2(self) -> int:
        with self.open_input() as file:
            content = file.read()
            numbers, symbols = parse_objects(content)

            ratios_sum = 0
            for symbol in symbols:
                adjacent_symbols = get_adjacent_cordinates(symbol.start)

                adjacent_numbers = set(
                    number
                    for number in numbers
                    for indice in number.indices
                    if indice in adjacent_symbols
                )  # Find all numbers adjacent to symbol

                if len(adjacent_numbers) == 2:
                    adjacent_numbers_list = list(adjacent_numbers)
                    gear_ratio = int(adjacent_numbers_list[0].value) * int(
                        adjacent_numbers_list[1].value
                    )
                    ratios_sum += gear_ratio

            return ratios_sum
