"""Common classes used in solving AoC challenges."""

from abc import ABC, abstractmethod
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, TextIO


class Aoc(ABC):
    """Helper class for solving AoC challenges.

    Args:
        input_file (str): Challenge input text file path.

    """

    def __init__(self, input_file: str | Path) -> None:
        self._input_file = input_file

    @abstractmethod
    def part_1(self) -> int:
        """Solves first part of task for given day."""

        raise NotImplementedError

    @abstractmethod
    def part_2(self) -> int:
        """Solves second part of task for given day."""

        raise NotImplementedError

    @contextmanager
    def open_input(self) -> Generator[TextIO, None, None]:
        """Opens provided task input file."""

        with open(self._input_file, "rt", encoding="utf-8") as file:
            yield file
