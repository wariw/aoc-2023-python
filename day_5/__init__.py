import re
from dataclasses import dataclass
from functools import partial
from itertools import islice
from typing import Iterable


@dataclass
class Map:
    source: range
    target: range


def find_locations(seeds: Iterable[int], mappings: list[list[Map]]) -> list[int]:
    locations: list[int] = []

    for seed_id in seeds:
        value = seed_id
        for mapping in mappings:
            value = find_in_map(mapping, value)

        locations.append(value)

    return locations


def find_in_map(maps: list[Map], source_value: int) -> int:
    for mapping in maps:
        if source_value in mapping.source:
            source_index = mapping.source.index(source_value)
            target_value = mapping.target[source_index]

            return target_value

    return source_value


def parse_mappings(sections: list[str]) -> dict[str, list[Map]]:
    mappings_dict: dict[str, list[Map]] = {}
    for mappings in sections:
        map_groups = mappings.split("\n")
        source, target = re.findall(r"(.*)\-to\-(.*) map\:", map_groups[0])[0]

        mappings_list: list[Map] = []
        for mapping in map_groups[1:]:
            if mapping:
                target_start, source_start, map_range = (
                    int(value) for value in mapping.split()
                )
                tmap = Map(
                    source=range(source_start, source_start + map_range),
                    target=range(target_start, target_start + map_range),
                )
                mappings_list.append(tmap)

        mappings_dict[f"{source}-{target}"] = mappings_list

    return mappings_dict


def convert_range(input_range: range, mappings: list[Map]) -> list[range]:
    """Converts single range according to mappings.

    Args:
        input_range (range): Input range of data.
        mappings (list[Map]): Conversions mappings.

    Returns:
        list[range]: Converted values.

    """
    converted_ranges = []
    unconverted_ranges = [input_range]

    for mapping in mappings:
        new_unconverted_ranges = []

        for unconverted_range in unconverted_ranges:
            new_unconverted_ranges.clear()
            intersection = range(
                max(unconverted_range.start, mapping.source.start),
                min(unconverted_range.stop, mapping.source.stop),
            )
            if len(intersection) != 0:
                low_index = unconverted_range.index(intersection.start)

                if low_index > 0:
                    new_unconverted_ranges.append(
                        range(unconverted_range.start, unconverted_range[low_index])
                    )

                high_index = unconverted_range.index(intersection.stop - 1)

                if high_index < len(unconverted_range) - 1:
                    new_unconverted_ranges.append(
                        range(unconverted_range[high_index], unconverted_range.stop)
                    )

                source_start = mapping.source.index(intersection.start)
                source_stop = mapping.source.index(intersection.stop - 1)

                converted_ranges.append(
                    range(
                        mapping.target[source_start],
                        mapping.target[source_stop] + 1,
                    )
                )
            else:
                new_unconverted_ranges = [unconverted_range]

        unconverted_ranges = new_unconverted_ranges

    return converted_ranges + unconverted_ranges


def parse_seed_ranges(seed_ranges: list[range], mapping_list: list[list[Map]]):
    parsed_ranges = seed_ranges

    for mappings in mapping_list:
        converted_ranges = []
        for seed_range in parsed_ranges:
            converted_range = convert_range(seed_range, mappings)
            converted_ranges.extend(converted_range)

        parsed_ranges = converted_ranges

    return parsed_ranges


def part_1() -> int:
    with open("day_5/input.txt", "rt") as file:
        content = file.read()

        groups = content.split("\n\n")

        seeds_ids = [int(seed) for seed in groups[0][7:].split()]
        mappings_dict = parse_mappings(groups[1:])

        locations = find_locations(seeds_ids, list(mappings_dict.values()))

        return min(locations)


def part_2() -> int:
    with open("day_5/input.txt", "rt") as file:
        content = file.read()

        groups = content.split("\n\n")

        seeds_id_ranges = [int(seed) for seed in groups[0][7:].split()]
        mappings_dict = parse_mappings(groups[1:])

        seed_groups = iter(
            partial(lambda it: tuple(islice(it, 2)), iter(seeds_id_ranges)), ()
        )  # Splits list into 2 value sublists.
        seed_ranges = [
            range(seed_group[0], seed_group[0] + seed_group[1])
            for seed_group in seed_groups
        ]

        parsed_ranges = parse_seed_ranges(seed_ranges, list(mappings_dict.values()))

        location = min(location_range.start for location_range in parsed_ranges)
        return location


if __name__ == "__main__":
    print(part_1())
    print(part_2())
