from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Flag
from itertools import count
from math import lcm
from typing import Generator, NamedTuple, Optional

from ._common import Aoc


class Day20(Aoc):
    def part_1(self):
        with self.open_input() as file:
            module_configuration = file.read()

            machines = parse_configuration(module_configuration)

            pulses: list[Pulse] = []
            for _ in range(1000):
                signals: list[Signal] = [Signal("button", "broadcaster", Pulse.LOW)]

                while signals:
                    signal = signals.pop(0)
                    pulses.append(signal.pulse)
                    new_signals = _process_signal(signal, machines)
                    signals.extend(new_signals)

            counts = Counter(pulses)

        return counts[Pulse.LOW] * counts[Pulse.HIGH]

    def part_2(self) -> int:
        with self.open_input() as file:
            module_configuration = file.read()

            machines = parse_configuration(module_configuration)

            rx_conjunctor = [name for name, machine in machines.items() if "rx" in machine.targets][0]
            rx_conjunctors = [name for name, machine in machines.items() if rx_conjunctor in machine.targets]

            first_pulses: dict[str, Optional[int]] = {c: None for c in rx_conjunctors}
            for button_press in count(1):
                signals: list[Signal] = [Signal("button", "broadcaster", Pulse.LOW)]

                while signals:
                    signal = signals.pop(0)

                    new_signals = _process_signal(signal, machines)

                    for new_signal in new_signals:
                        if (
                            new_signal.sender in rx_conjunctors
                            and new_signal.pulse == Pulse.HIGH
                            and not first_pulses[new_signal.sender]
                        ):
                            first_pulses[new_signal.sender] = button_press

                    signals.extend(new_signals)

                if all(first_pulses.values()):
                    break

        return lcm(*first_pulses.values())


class Pulse(Flag):
    LOW = False
    HIGH = True


class Signal(NamedTuple):
    sender: str
    target: str
    pulse: Pulse

    def __repr__(self):
        return f"{self.sender} -{'low' if self.pulse == Pulse.LOW else 'high'}-> {self.target}"


class State(Flag):
    OFF = False
    ON = True


class Machine(NamedTuple):
    module: Module
    targets: tuple

    def process_signal(self, pulse: Pulse, source: str = "") -> Generator[tuple[str, Pulse], ...]:
        pulse = self.module.process_pulse(pulse, source)

        if pulse is not None:
            return ((target, pulse) for target in self.targets)

        return (_ for _ in ())


class Module:
    def process_pulse(self, pulse: Pulse, source: str = "") -> Optional[Pulse]:
        raise NotImplementedError


@dataclass
class FlipFlop(Module):
    state: State = State.OFF

    def process_pulse(self, pulse: Pulse, source: str = "") -> Optional[Pulse]:
        if pulse == Pulse.HIGH:
            return None

        self.state = State(~self.state)

        return Pulse(self.state.value)


class Conjunction(Module):
    def __init__(self):
        self.states: dict[str, Pulse] = {}

    def connect_source(self, source: str) -> None:
        self.states[source] = Pulse.LOW

    def process_pulse(self, pulse: Pulse, source: str = "") -> Optional[Pulse]:
        self.states[source] = pulse

        return Pulse(not all(self.states.values()))


class Broadcast(Module):
    def process_pulse(self, pulse: Pulse, source: str = "") -> Optional[Pulse]:
        return pulse


def parse_configuration(config: str) -> dict[str, Machine]:
    """Parses configuration text input into machine objects."""

    modules: dict[str, Machine] = {}

    for line in config.splitlines():
        module_text, targets = line.split(" -> ")

        targets = targets.replace(" ", "").split(",")

        if module_text == "broadcaster":
            module = Broadcast()
            name = "broadcaster"
        elif module_text[0] == "%":
            module = FlipFlop()
            name = module_text[1:]
        else:
            module = Conjunction()
            name = module_text[1:]

        modules[name] = Machine(module, tuple(targets))

    # Configure sources for conjunction machines
    conjunctions = {name: machine for name, machine in modules.items() if isinstance(machine.module, Conjunction)}

    for name, machine in conjunctions.items():
        sources = [name_ for name_, machine_ in modules.items() if name in machine_.targets]

        for source in sources:
            machine.module.connect_source(source)

    return modules


def _process_signal(signal: Signal, machines: dict[str, Machine]) -> list[Signal]:
    try:
        machine = machines[signal.target]
    except KeyError:
        return []

    return [
        Signal(signal.target, new_target, new_pulse)
        for new_target, new_pulse in machine.process_signal(signal.pulse, source=signal.sender)
    ]
