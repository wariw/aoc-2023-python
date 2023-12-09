import re
from dataclasses import dataclass

from ._common import Aoc


@dataclass(frozen=True, eq=True)
class Cordinate:
    row: int
    position: int


@dataclass(frozen=True, eq=True)
class CordinateObject:
    value: int | str
    start: Cordinate
    span: int

    @property
    def indices(self) -> list[Cordinate]:
        return [
            Cordinate(self.start.row, self.start.position + index)
            for index in range(self.span)
        ]


def parse_numbers(parts_map: str) -> set[CordinateObject]:
    map_rows = parts_map.splitlines()
    cordinates: set[CordinateObject] = set()
    for row_index, map_row in enumerate(map_rows):
        for match in re.finditer(r"(\d+)", map_row):
            cordinate = CordinateObject(
                int(match.group()),
                Cordinate(row_index, match.start()),
                match.end() - match.start(),
            )
            cordinates.add(cordinate)

    return cordinates


def parse_symbols(parts_map: str) -> set[CordinateObject]:
    map_rows = parts_map.splitlines()
    cordinates = set()
    for row_index, map_row in enumerate(map_rows):
        for match in re.finditer(r"(?!\.)\W", map_row):
            cordinate = CordinateObject(
                match.group(),
                Cordinate(row_index, match.start()),
                match.end() - match.start(),
            )
            cordinates.add(cordinate)

    return cordinates


def get_adjacent_cordinates(cordinate: Cordinate) -> set[Cordinate]:
    adjacent = [
        Cordinate(cordinate.row + i, cordinate.position + j)
        for i in (-1, 0, 1)
        for j in (-1, 0, 1)
        if i != 0 or j != 0
    ]

    return set(adjacent)


def get_part_number_cordinates(symbols: set[CordinateObject]):
    number_cordinates: set[Cordinate] = set()
    for symbol in symbols:
        adjacent = get_adjacent_cordinates(symbol.start)
        number_cordinates.update(adjacent)

    return number_cordinates


class Day3(Aoc):
    def part_1(self) -> int:
        with self.open_input() as file:
            content = file.read()
            numbers = parse_numbers(content)
            symbols = parse_symbols(content)

            part_cordinates = get_part_number_cordinates(symbols)

            parts: set[CordinateObject] = set()

            for part in numbers:
                for cordinate in part.indices:
                    if cordinate in part_cordinates:
                        parts.add(part)

            parts_sum = 0
            for part in parts:
                parts_sum += int(part.value)

            return parts_sum

    def part_2(self) -> int:
        with self.open_input() as file:
            content = file.read()
            numbers = parse_numbers(content)
            symbols = parse_symbols(content)

            ratios_sum = 0
            for symbol in symbols:
                adjacent = get_adjacent_cordinates(symbol.start)

                adjacent_numbers = set()
                for number in numbers:
                    for indice in number.indices:
                        if indice in adjacent:
                            adjacent_numbers.add(number)

                if len(adjacent_numbers) == 2:
                    adjacent_numbers_list = list(adjacent_numbers)
                    gear_ratio = (
                        adjacent_numbers_list[0].value * adjacent_numbers_list[1].value
                    )
                    ratios_sum += gear_ratio

            return ratios_sum