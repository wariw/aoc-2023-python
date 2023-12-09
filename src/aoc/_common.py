from contextlib import contextmanager
from pathlib import Path


class Aoc:
    def __init__(self, input_file: str | Path) -> None:
        self._input_file = input_file

    def part_1(self) -> int:
        raise NotImplementedError

    def part_2(self) -> int:
        raise NotImplementedError

    @contextmanager
    def open_input(self):
        with open(self._input_file, "rt", encoding="utf-8") as file:
            yield file
