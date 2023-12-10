from math import lcm
from itertools import cycle

from ._common import Aoc


class Day8(Aoc):
    def part_1(self) -> int:
        with self.open_input() as file:
            lines = file.read().splitlines()
            instructions, nodes = _parse_inputs(lines)

            counter = calculate_steps(nodes, instructions, "AAA", "ZZZ")

        return counter

    def part_2(self) -> int:
        with self.open_input() as file:
            lines = file.read().splitlines()
            instructions, nodes = _parse_inputs(lines)

            ghosts = [node[:2] for node in nodes if node[2] == "A"]

            ghosts_steps = [
                calculate_steps(nodes, instructions, ghost + "A", "Z")
                for ghost in ghosts
            ]

            common_steps = lcm(*ghosts_steps)

        return common_steps


def calculate_steps(
    nodes: dict[str, tuple[str, str]],
    instructions: str,
    start: str = "AAA",
    finish: str = "ZZZ",
) -> int:
    """Calculates number of steps required to go from start to finish according to instructions.

    Args:
        nodes (dict[str, tuple[str, str]]): Map of nodes.
        instructions (str): Set of instruction to follow.
        start (str, optional): Start node. Defaults to "AAA".
        finish (str, optional):
            Finish node. Checks only last part if less than 3. Defaults to "ZZZ".

    Returns:
        int: Number of steps.

    """
    node = start
    counter = 0
    for instruction in cycle(instructions):
        counter += 1
        directions = nodes[node]
        node = directions[0] if instruction == "L" else directions[1]

        if node[-len(finish) :] == finish:
            break

    return counter


def _parse_inputs(inputs: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    instructions = inputs[0]

    nodes = {}
    for inpt in inputs[2:]:
        node = inpt[:3]
        directions = (inpt[7:10], inpt[12:15])
        nodes[node] = directions

    return instructions, nodes
