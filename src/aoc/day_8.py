from math import lcm
from itertools import cycle

from ._common import Aoc


def parse_inputs(inputs: list[str]) -> dict[str, tuple[str, str]]:
    nodes = {}
    for inpt in inputs:
        node = inpt[:3]
        directions = (inpt[7:10], inpt[12:15])
        nodes[node] = directions

    return nodes


class Day8(Aoc):
    def part_1(self) -> int:
        with self.open_input() as file:
            lines = file.read().splitlines()
            instructions = lines[0]
            nodes = parse_inputs(lines[2:])

            node = "AAA"
            counter = 0
            for instruction in cycle(instructions):
                counter += 1
                directions = nodes[node]
                node = directions[0] if instruction == "L" else directions[1]

                if node == "ZZZ":
                    break

        return counter

    def part_2(self) -> int:
        with self.open_input() as file:
            lines = file.read().splitlines()
            instructions = lines[0]
            nodes = parse_inputs(lines[2:])

            ghosts = [node[:2] for node in nodes if node[2] == "A"]
            ghost_nodes = {ghost: ghost + "A" for ghost in ghosts}
            ghost_counters = {}

            for ghost in ghosts:
                ghost_counters[ghost] = 0
                for instruction in cycle(instructions):
                    ghost_counters[ghost] += 1
                    node = ghost_nodes[ghost]
                    directions = nodes[node]
                    ghost_nodes[ghost] = (
                        directions[0] if instruction == "L" else directions[1]
                    )
                    if ghost_nodes[ghost][2] == "Z":
                        break

            common_steps = lcm(*ghost_counters.values())

        return common_steps
