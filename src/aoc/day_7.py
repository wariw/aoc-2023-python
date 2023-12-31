from collections import Counter
from dataclasses import dataclass
from enum import Enum, IntEnum
from operator import itemgetter
from typing import cast, Iterable, Self

from ._common import Aoc


class Card(IntEnum):
    "Card type."

    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2
    JOKER = 1


TypeHand = tuple[Card, Card, Card, Card, Card]


class HandType(Enum):
    """Type of hand."""

    POKER = 6
    FOUR = 5
    FULL_HOUSE = 4
    THREE = 3
    TWO_PAIR = 2
    PAIR = 1
    HIGH_CARD = 0


@dataclass
class Hand:
    """Represents hand of cards."""

    cards: TypeHand

    def __eq__(self, other: Self):
        if self.hand_type.value == other.hand_type.value:
            for index, card in enumerate(self.cards):
                if other.cards[index].value != card.value:
                    return False

            return True

        return False

    def __lt__(self, other: Self):
        if self.hand_type.value == other.hand_type.value:
            for index, card in enumerate(self.cards):
                card_value = card.value
                other_value = other.cards[index].value
                if card_value != other_value:
                    return card_value < other_value

            return False

        return self.hand_type.value < other.hand_type.value

    def __repr__(self) -> str:
        return "".join(repr(self.cards))

    @property
    def hand_type(self) -> HandType:
        """Type of hand."""
        cards = self.cards
        if Card.JOKER in self.cards:
            cards = replace_jokers(cards)

        hand_type = find_hand_type(cards)

        return hand_type


class Day7(Aoc):
    def part_1(self) -> int:
        with self.open_input() as file:
            lines = file.read().splitlines()

            hands = []

            for line in lines:
                cards_string, bid = line.split()

                cards = _parse_cards(cards_string)
                cards = cast(TypeHand, cards)
                hand = Hand(cards)
                hands.append((int(bid), hand))

            sorted_hands = sorted(hands, key=itemgetter(1))

            winning_sum = 0

            for index, sorted_hand in enumerate(sorted_hands):
                hand_win = (index + 1) * sorted_hand[0]
                winning_sum += hand_win

        return winning_sum

    def part_2(self) -> int:
        with self.open_input() as file:
            lines = file.read().splitlines()

            hands = []

            for line in lines:
                cards_string, bid = line.split()

                cards = _parse_cards(cards_string, jokers=True)
                cards = cast(TypeHand, cards)
                hand = Hand(cards)
                hands.append((int(bid), hand))

            sorted_hands = sorted(hands, key=itemgetter(1))

            winning_sum = 0

            for index, sorted_hand in enumerate(sorted_hands):
                hand_win = (index + 1) * sorted_hand[0]
                winning_sum += hand_win

        return winning_sum


def parse_card(card: str, jokers: bool = False) -> Card:
    """Parses card symbol into Card enum.

    Args:
        card (str): Symbol of card.
        jokers (bool, optional): Decides if 'J' should be parsed as Jocker. Defaults to False.

    Returns:
        Card: Card enum.
    """

    try:
        card_val = int(card[0])
        return Card(card_val)
    except ValueError:
        match card:
            case "A":
                return Card.ACE
            case "K":
                return Card.KING
            case "Q":
                return Card.QUEEN
            case "J":
                return Card.JOKER if jokers else Card.JACK
            case "T":
                return Card.TEN
            case _:
                raise


def find_hand_type(cards: Iterable[Card]) -> HandType:
    """Finds type of hand.

    Args:
        cards (Iterable[Card]): Cards in hand.

    Raises:
        ValueError: In case of unparsable hand type.

    Returns:
        HandType: Type of hand.

    """
    card_counts = Counter(cards)
    duplicates = [value for value in card_counts.values() if value > 1]
    parsing_error = ValueError("Unparsable Hand")

    match len(duplicates):
        case 0:
            return HandType.HIGH_CARD
        case 1:
            match sum(duplicates):
                case 2:
                    return HandType.PAIR
                case 3:
                    return HandType.THREE
                case 4:
                    return HandType.FOUR
                case 5:
                    return HandType.POKER
                case _:
                    raise parsing_error
        case 2:
            return HandType.TWO_PAIR if sum(duplicates) == 4 else HandType.FULL_HOUSE
        case _:
            raise parsing_error


def replace_jokers(cards: Iterable[Card]) -> tuple[Card, ...]:
    """Replace jokers in hand with cards providing highest hand type.

    Args:
        cards (Iterable[Card]): Cards to parse.

    Raises:
        ValueError: In case of unparsable hand.

    Returns:
        tuple[Card, ...]: Cards with jokers replaced.

    """
    jokerless = list(filter(lambda card: card != Card.JOKER, cards))
    hand_type = find_hand_type(jokerless)

    if jokerless:
        match hand_type:
            case HandType.HIGH_CARD:
                highest_card = max(card for card in list(jokerless))
                return tuple(
                    map(
                        lambda x: highest_card if x is Card.JOKER else x,
                        cards,
                    )
                )
            case HandType.PAIR | HandType.THREE | HandType.FOUR:
                card_counts = Counter(jokerless)
                duplicates = [
                    (index, value) for index, value in card_counts.items() if value > 1
                ]
                sorted_duplicates = sorted(duplicates, key=itemgetter(1))
                return tuple(
                    map(
                        lambda x: sorted_duplicates[0][0] if x is Card.JOKER else x,
                        cards,
                    )
                )
            case HandType.TWO_PAIR:
                card_counts = Counter(jokerless)
                duplicates = [value for value in card_counts.keys() if value > 1]
                higher_duplicate = max(*duplicates)
                return tuple(
                    map(
                        lambda x: higher_duplicate if x is Card.JOKER else x,
                        cards,
                    )
                )
            case _:
                raise ValueError
    else:
        return (Card.ACE, Card.ACE, Card.ACE, Card.ACE, Card.ACE)


def _parse_cards(cards: str, jokers: bool = False) -> tuple[Card, ...]:
    return tuple(parse_card(card, jokers) for card in [*cards])
