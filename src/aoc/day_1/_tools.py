import re

numbers_text = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

digits_pattern = re.compile(r"\d")
string_pattern = re.compile(rf"(?=(\d|{'|'.join(list(numbers_text))}))")


def _convert_match(text: str) -> int:
    try:
        return int(text)
    except ValueError:
        return numbers_text[text]


def decode_cordinate(encoded_cordinate: str, /, parse_text: bool = False) -> int:
    """Decodes cordinate from string encoded data.

    Example:
        a1b2c3d4e5f -> 15

    Args:
        encoded_cordinate (str): Encoded cordinate data.
        parse_text (bool, optional): Decides if digits in text form should be parsed. Defaults to False.

    Returns:
        int: Parsed cordinate.

    """
    matches = re.findall(
        string_pattern if parse_text else digits_pattern, encoded_cordinate
    )
    numbers = list(map(_convert_match, matches))
    cordinate = 10 * numbers[0] + numbers[-1]

    return cordinate
