from aoc._common import Aoc
from ._tools import decode_cordinate


class Day1(Aoc):
    def part_1(self) -> int:
        with self.open_input() as file:
            lines = file.read().splitlines()
            cordinate_sum = 0
            for line in lines:
                cordinate_sum += decode_cordinate(line)

            return cordinate_sum

    def part_2(self) -> int:
        with self.open_input() as file:
            lines = file.read().splitlines()
            cordinate_sum = 0
            for line in lines:
                cordinate_sum += decode_cordinate(line, parse_text=True)

            return cordinate_sum
