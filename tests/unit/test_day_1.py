from pytest import mark

from aoc.day_1._tools import decode_cordinate


@mark.parametrize(
    "encoded_cordinate, decoded_cordinate",
    (
        ("1abc2", 12),
        ("pqr3stu8vwx", 38),
        ("a1b2c3d4e5f", 15),
        ("treb7uchet", 77),
    ),
)
def test_decode_cordinate(encoded_cordinate, decoded_cordinate):
    assert decode_cordinate(encoded_cordinate) == decoded_cordinate


@mark.parametrize(
    "encoded_cordinate, decoded_cordinate",
    (
        ("two1nine", 29),
        ("eightwothree", 83),
        ("abcone2threexyz", 13),
        ("xtwone3four", 24),
        ("4nineeightseven2", 42),
        ("zoneight234", 14),
        ("7pqrstsixteen", 76),
    ),
)
def test_decode_cordinate_textual(encoded_cordinate, decoded_cordinate):
    assert decode_cordinate(encoded_cordinate, parse_text=True) == decoded_cordinate
