from ._common import Aoc


def find_solutions(time: int, distance: int) -> list[int]:
    """Finds solutions how to win races for specified parameters.

    Args:
        time (int): Total race time [ms].
        distance (int): Top distance [mm].

    Returns:
        list[int]: List of button hold times [ms].

    """
    return [hold for hold in range(time) if hold * (time - hold) > distance]


class Day6(Aoc):
    def part_1(self) -> int:
        with self.open_input() as file:
            content = file.read().splitlines()

            times = [int(value) for value in content[0].split()[1:]]
            distances = [int(value) for value in content[1].split()[1:]]

            races = zip(times, distances)

            error_margin = 1

            for race in races:
                solutions = find_solutions(*race)
                error_margin *= len(solutions)

            return error_margin

    def part_2(self) -> int:
        with self.open_input() as file:
            content = file.read().splitlines()

            time = int("".join(content[0].split()[1:]))
            distance = int("".join(content[1].split()[1:]))

            solutions = find_solutions(time, distance)

            return len(solutions)
