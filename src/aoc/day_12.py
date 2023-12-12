import re
from functools import cache
from itertools import chain, repeat

from ._common import Aoc


class Day12(Aoc):
    def part_1(self):
        with self.open_input() as file:
            condition_records = file.read().splitlines()

            total_combinations = 0
            for record in condition_records:
                data, nums = record.split(" ")
                nums = tuple(int(num) for num in nums.split(","))

                total_combinations += count_combinations(data, nums)

        return total_combinations

    def part_2(self) -> int:
        with self.open_input() as file:
            condition_records = file.read().splitlines()

            total_combinations = 0
            for index, record in enumerate(condition_records):
                data, nums = record.split(" ")
                nums = tuple(int(num) for num in nums.split(","))

                data = "?".join(repeat(data, 5))
                nums = tuple(chain.from_iterable(repeat(nums, 5)))

                total_combinations += count_combinations(data, nums)

                print(f"{index + 1} of {len(condition_records)}")

        return total_combinations


@cache
def count_combinations(data: str, nums: tuple[int]) -> int:
    characters = len(data)
    number = nums[0]

    counter = 0
    if len(nums) > 1:
        for index in range(characters):
            sequence = "".join(repeat(".", index)) + "".join(repeat("#", number)) + "."

            if not is_sequence_valid(sequence, data[: len(sequence)]):
                continue

            data_left = data[len(sequence) :]
            counter += count_combinations(data_left, nums[1:])
    else:
        for index in range(characters - number + 1):
            sequence = (
                "".join(repeat(".", index))
                + "".join(repeat("#", number))
                + "".join(repeat(".", characters - number - index))
            )
            if not is_sequence_valid(sequence, data):
                continue

            counter += 1

    return counter


@cache
def is_sequence_valid(sequence: str, validator: str) -> bool:
    if "#" in validator or "." in validator:
        pattern = validator.replace(".", r"\.")
        pattern = pattern.replace("?", ".")
        match = re.match(pattern, sequence)

        if not match:
            return False

    return True
