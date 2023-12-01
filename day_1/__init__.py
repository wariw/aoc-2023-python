from ._tools import decode_cordinate, decode_cordinate_textual


def part_1() -> int:
    with open("day_1/input.txt", "rt") as file:
        lines = file.read().splitlines()
        cordinate_sum = 0
        for line in lines:
            cordinate_sum += decode_cordinate(line)

        return cordinate_sum


def part_2() -> int:
    with open("day_1/input.txt", "rt") as file:
        lines = file.read().splitlines()
        cordinate_sum = 0
        for line in lines:
            cordinate_sum += decode_cordinate_textual(line)

        return cordinate_sum
