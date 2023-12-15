from collections import defaultdict, OrderedDict

from ._common import Aoc


class Day15(Aoc):
    def part_1(self):
        with self.open_input() as file:
            sequence = file.read().rstrip("\n")
            steps = sequence.split(",")

        return sum(calculate_hash(step) for step in steps)

    def part_2(self) -> int:
        with self.open_input() as file:
            sequence = file.read().rstrip("\n")

            boxes: defaultdict[int, OrderedDict[str, int]] = defaultdict(
                OrderedDict[str, int]
            )

            for step in sequence.split(","):
                label, focal = step.split("-") if "-" in step else step.split("=")
                box = calculate_hash(label)

                if focal:
                    boxes[box][label] = int(focal)
                else:
                    if label in boxes[box]:
                        del boxes[box][label]

            total_power = 0
            for box, lenses in boxes.items():
                for index, lens in enumerate(lenses.values()):
                    total_power += (box + 1) * (index + 1) * lens

        return total_power


def calculate_hash(text: str) -> int:
    """Calculates hash for given string."""

    current_value = 0

    for char in text:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256

    return current_value
