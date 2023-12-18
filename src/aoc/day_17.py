from collections import defaultdict
from heapq import heappush, heappop
from typing import Self, NamedTuple

from ._common import Aoc
from .tools.coordinates import Coordinate, Direction


class Node(NamedTuple):
    location: Coordinate
    direction: Direction
    steps: int

    def __repr__(self):
        return f"{self.location!r} {self.direction!r}{self.steps}"

    def __lt__(self, other: Self):
        return self.steps < other.steps

    @property
    def possible_directions(self) -> list[Direction]:
        possible_directions = [self.direction.rotate(), self.direction.rotate(False)]

        if self.steps != 3:
            possible_directions.append(self.direction)

        return possible_directions


class UltraNode(Node):
    @property
    def possible_directions(self) -> list[Direction]:
        if self.steps < 4:
            return [self.direction]

        possible_directions = [self.direction.rotate(), self.direction.rotate(False)]

        if self.steps != 10:
            possible_directions.append(self.direction)

        return possible_directions


class Day17(Aoc):
    def part_1(self):
        with self.open_input() as file:
            traffic_map = file.read()

            start = Coordinate(0, 0)
            end = Coordinate(len(traffic_map.splitlines()) - 1, len(traffic_map.splitlines()[0]) - 1)

            length = shortest_path(start, end, traffic_map)

        return length

    def part_2(self) -> int:
        with self.open_input() as file:
            traffic_map = file.read()

            start = Coordinate(0, 0)
            end = Coordinate(len(traffic_map.splitlines()) - 1, len(traffic_map.splitlines()[0]) - 1)

            length = shortest_path(start, end, traffic_map, ultra=True)

        return length


def shortest_path(start: Coordinate, finish: Coordinate, traffic_map: str, ultra: bool = False) -> int:
    _Node = UltraNode if ultra else Node

    visited_nodes: set[tuple[int, Node]] = set()
    heat_loss: dict[Node, float] = defaultdict(lambda: float("infinity"))
    next_nodes: list[tuple[int, Node]] = []

    for direction in {Direction.RIGHT, Direction.DOWN}:
        node = (_get_cost(start + direction.value, traffic_map), _Node(start + direction.value, direction, 1))
        heappush(next_nodes, node)

    while len(next_nodes):
        cost, node = heappop(next_nodes)

        visited_nodes.add((cost, node))

        if node.location == finish:
            return cost

        for direction in node.possible_directions:
            new_cord = node.location + direction.value

            if start.position <= new_cord.position <= finish.position and start.row <= new_cord.row <= finish.row:
                steps = node.steps + 1 if direction == node.direction else 1
                new_node = _Node(new_cord, direction, steps)
                new_cost = cost + _get_cost(new_cord, traffic_map)
                new_location = (new_cost, new_node)

                if new_cost < heat_loss[new_node]:
                    heat_loss[new_node] = new_cost
                    heappush(next_nodes, new_location)


def _get_cost(coordinate: Coordinate, traffic_map: str) -> int:
    return int(traffic_map.splitlines()[coordinate.row][coordinate.position])
