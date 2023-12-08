from math import lcm
from itertools import cycle


def parse_inputs(inputs: list[str]) -> dict[str, tuple[str, str]]:
    nodes = {}
    for inpt in inputs:
        node = inpt[:3]
        directions = (inpt[7:10], inpt[12:15])
        nodes[node] = directions

    return nodes


def part_1() -> int:
    with open("day_8/input.txt", "rt") as file:
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


def part_2() -> int:
    with open("day_8/input.txt", "rt") as file:
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


if __name__ == "__main__":
    print(part_1())
    print(part_2())
