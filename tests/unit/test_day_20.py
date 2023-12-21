from pytest import mark

from aoc.day_20 import Conjunction, Pulse


@mark.parametrize(
    "signals,response",
    (
        ((("a", Pulse.HIGH),), Pulse.HIGH),
        ((("a", Pulse.LOW),), Pulse.HIGH),
        ((("a", Pulse.LOW), ("b", Pulse.HIGH)), Pulse.HIGH),
        ((("a", Pulse.LOW), ("b", Pulse.HIGH), ("a", Pulse.HIGH)), Pulse.LOW),
    ),
)
def test_conjunction(signals, response):
    module = Conjunction()
    module.connect_source("a")
    module.connect_source("b")
    ret = None

    for source, pulse in signals:
        ret = module.process_pulse(pulse, source)

    assert ret == response
