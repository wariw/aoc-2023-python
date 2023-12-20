from dataclasses import asdict, dataclass, replace
from numbers import Number
from math import prod
from operator import gt, lt
from typing import Callable, Optional, NamedTuple

from ._common import Aoc


class Day19(Aoc):
    def part_1(self):
        with self.open_input() as file:
            rules, parts = file.read().split("\n\n")

            workflows = _parse_workflows(rules)
            parts = _parse_parts(parts)

        return sum(part.rating for part in parts if _process_part(part, workflows))

    def part_2(self) -> int:
        with self.open_input() as file:
            rules, parts = file.read().split("\n\n")

            workflows = _parse_workflows(rules)
            part = PartRanges(*[range(1, 4001)] * 4)

            to_process = [(part, "in")]
            accepted = []
            while to_process:
                next_process: list[tuple[PartRanges, str]] = []

                for part, label in to_process:
                    processed = process_part_ranges(part, workflows[label])

                    for proc, label_ in processed:
                        if label_ == "A":
                            accepted.append(proc)
                        elif label_ == "R":
                            pass
                        else:
                            next_process.append((proc, label_))

                to_process = next_process

        return sum(part.rating for part in accepted)


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @property
    def rating(self) -> int:
        return sum(asdict(self).values())


@dataclass
class PartRanges:
    x: range
    m: range
    a: range
    s: range

    @property
    def rating(self) -> int:
        return prod(len(value) for value in asdict(self).values())


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


def process_part_ranges(part: PartRanges, workflow: Workflow) -> list[tuple[PartRanges, str]]:
    returned: list[tuple[PartRanges, str]] = []
    parts = [part]

    for rule in workflow.rules:
        for part in parts:
            parts.remove(part)
            a, r = _apply_rule(part, rule)

            if a:
                returned.append((a, rule.target))
            if r:
                parts.append(r)

    return returned + [(part, workflow.default) for part in parts]


def split_range(rng: range, value: int) -> tuple[range, range]:
    """Splits range into two ranges by specified value."""

    return range(rng.start, value), range(value, rng.stop)


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
        for rule_ in rules[:-1]:
            comp, target = rule_.split(":")
            prop = comp[0]
            operation = lt if comp[1] == "<" else gt
            value = int(comp[2:])
            rule = Rule(prop, operation, value, target)

            rls.append(rule)

        workflows[name] = Workflow(rls, rules[-1])

    return workflows


def _process_part(part: Part, workflows: dict[str, Workflow]) -> bool:
    next_label = "in"
    while next_label != "R":
        next_label = process_part(part, workflows[next_label])

        if next_label == "A":
            return True

    return False


def _apply_rule(part: PartRanges, rule: Rule) -> tuple[Optional[PartRanges], Optional[PartRanges]]:
    value: range = getattr(part, rule.prop)

    if rule.value in value:
        ranges = split_range(value, rule.value + (1 if rule.condition == gt else 0))
        parts = [replace(part, **{rule.prop: rng}) for rng in ranges]
    else:
        parts = [part, None]

    if rule.condition == gt:
        parts = reversed(parts)

    return tuple(parts)
