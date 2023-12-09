import re

numbers = {
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


def decode_cordinate(encoded_cordinate: str) -> int:
    matches = re.findall(r"\d", encoded_cordinate)
    cordinate = 10 * int(matches[0]) + int(matches[-1])

    return cordinate


def decode_cordinate_textual(encoded_cordinate: str) -> int:
    matches = re.findall(rf"(?=(\d|{'|'.join(list(numbers))}))", encoded_cordinate)

    def _convert_text(text: str | int) -> int:
        try:
            return numbers[text]
        except KeyError:
            return text

    matches = list(map(_convert_text, matches))

    cordinate = 10 * int(matches[0]) + int(matches[-1])

    return cordinate
