import re


def increment_card_count(cards_counter: dict[int, int], card_id: int, count: int = 1):
    if card_id not in cards_counter:
        cards_counter[card_id] = 0

    cards_counter[card_id] = cards_counter[card_id] + count


def parse_card(card_data: str) -> tuple[int, list[int], list[int]]:
    """Parses card data string into id and number lists.

    Args:
        card_data (str): String representing card data.

    Returns:
        tuple: Parsed card data.

    """
    card_id, winning_string, guessed_string = re.findall(
        r"Card +(\d+): (.*) +\| (.*)", card_data
    )[0]
    winning_numbers = unpack_numbers(winning_string)
    guessed_numbers = unpack_numbers(guessed_string)

    return int(card_id), winning_numbers, guessed_numbers


def unpack_numbers(numbers_string: str) -> list[int]:
    numbers = [int(number) for number in numbers_string.split()]

    return numbers


def part_1() -> int:
    with open("day_4/input.txt", "rt") as file:
        content = file.read()

        points_sum = 0

        for card in content.splitlines():
            _, winning_numbers, guessed_numbers = parse_card(card)

            winning_set = set(winning_numbers)
            guessed_set = set(guessed_numbers)

            correct_numbers = winning_set & guessed_set
            correct_count = len(correct_numbers)

            if correct_count:
                card_value = 2 ** (correct_count - 1)
                points_sum += card_value

        return points_sum


def part_2() -> int:
    with open("day_4/input.txt", "rt") as file:
        content = file.read()

        card_copies = {}

        for card in content.splitlines():
            card_id, winning_numbers, guessed_numbers = parse_card(card)

            increment_card_count(card_copies, card_id)

            winning_set = set(winning_numbers)
            guessed_set = set(guessed_numbers)

            correct_numbers = winning_set & guessed_set
            correct_count = len(correct_numbers)

            for cards in range(correct_count):
                card_to_update = card_id + cards + 1
                current_card_value = card_copies[card_id]
                increment_card_count(card_copies, card_to_update, current_card_value)

        total_cards = sum(card_copies.values())

        return total_cards


if __name__ == "__main__":
    print(part_1())
    print(part_2())
