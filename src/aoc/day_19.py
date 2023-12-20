from numbers import Number
from operator import lt, gt
from typing import Callable, NamedTuple

from ._common import Aoc


class Day19(Aoc):
    def part_1(self):
        with self.open_input() as file:
            rules, parts = file.read().split("\n\n")

            workflows = _parse_workflows(rules)
            parts = _parse_parts(parts)

            accepted = [part for part in parts if _process_part(part, workflows)]

        return sum(part.rating for part in accepted)

    def part_2(self) -> int:
        with self.open_input() as file:
            rules, parts = file.read().split("\n\n")

            workflows = _parse_workflows(rules)
            part_range = range(1, 4000)
            part = PartRanges(*[part_range] * 4)

            to_process = [(part, "in")]
            while to_process:
                part, n = to_process[0]
                n = process_part_ranges(part, workflows[n])

                if n == "A":
                    return True

            accepted = [part for part in parts if _process_part(part, workflows)]

        return sum(part.rating for part in accepted)


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @property
    def rating(self) -> int:
        return self.x + self.m + self.a + self.s


class PartRanges(NamedTuple):
    x: range
    m: range
    a: range
    s: range

    @property
    def rating(self) -> int:
        return sum(self.x) + sum(self.m) + sum(self.a) + sum(self.s)


class Rule(NamedTuple):
    prop: str
    condition: Callable[[Number, Number], bool]
    value: int
    target: str


class Workflow(NamedTuple):
    rules: list[Rule]
    default: str


def process_part(part: Part, workflow: Workflow) -> str:
    for rule in workflow.rules:
        prop = getattr(part, rule.prop)

        if rule.condition(prop, rule.value):
            return rule.target

    return workflow.default


def process_part_ranges(parts: list[PartRanges], workflow: Workflow) -> str:
    returned: list[tuple[PartRanges, str]] = []

    for rule in workflow.rules:
        for part in parts:
            prop = getattr(part, rule.prop)

            if rule.condition(prop, rule.value):
                return rule.target

    return workflow.default


def _parse_parts(parts_text: str) -> list[Part]:
    parts = []
    for part_text in parts_text.splitlines():
        vals = part_text[1:-1].split(",")
        part = Part(*[int(val.split("=")[1]) for val in vals])

        parts.append(part)

    return parts


def _parse_workflows(rules_text: str) -> dict[str, Workflow]:
    workflows: dict[str, Workflow] = {}

    for rule_text in rules_text.splitlines():
        name, rules = rule_text.split("{")
        rules = rules[:-1].split(",")

        rls = []
        for rule in rules[:-1]:
            comp, target = rule.split(":")
            prop = comp[0]
            e = lt if comp[1] == "<" else gt
            v = int(comp[2:])
            r = Rule(prop, e, v, target)

            rls.append(r)

        workflows[name] = Workflow(rls, rules[-1])

    return workflows


def _process_part(part: Part, workflows: dict[str, Workflow]) -> bool:
    n = "in"
    while n != "R":
        n = process_part(part, workflows[n])

        if n == "A":
            return True

    return False
