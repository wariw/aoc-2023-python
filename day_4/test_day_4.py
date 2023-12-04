from pytest import mark

from day_4 import parse_card


@mark.parametrize(
    "card_string, card_id, winning_numbers, guessed_numbers",
    (
        (
            "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
            1,
            [41, 48, 83, 86, 17],
            [83, 86, 6, 31, 17, 9, 48, 53],
        ),
    ),
)
def test_decode_cordinate(card_string, card_id, winning_numbers, guessed_numbers):
    assert parse_card(card_string) == (card_id, winning_numbers, guessed_numbers)
