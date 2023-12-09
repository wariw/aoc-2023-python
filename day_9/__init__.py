def generate_diffs(data: list[int]) -> list[int]:
    diffs = []
    for index in range(len(data) - 1):
        diff = data[index + 1] - data[index]
        diffs.append(diff)

    return diffs


def part_1() -> int:
    with open("day_9/input.txt", "rt") as file:
        lines = file.read().splitlines()

        history_sets = []
        for line in lines:
            history_sets.append([int(value) for value in line.split()])

        interpolated_sum = 0

        for dataset in history_sets:
            diffs = [[*dataset]]
            while not all(diff == 0 for diff in diffs[-1]):
                diffs.append(generate_diffs(diffs[-1]))

            vals = [0]
            last_diffs = list(diff[-1] for diff in diffs)[:-1]
            last_diffs.reverse()
            for value in last_diffs:
                vals.append(vals[-1] + value)

            interpolated_sum += vals[-1]

    return interpolated_sum


def part_2() -> int:
    with open("day_9/input.txt", "rt") as file:
        lines = file.read().splitlines()

        history_sets = []
        for line in lines:
            history_sets.append([int(value) for value in line.split()])

        interpolated_sum = 0

        for dataset in history_sets:
            diffs = [[*dataset]]
            while not all(diff == 0 for diff in diffs[-1]):
                diffs.append(generate_diffs(diffs[-1]))

            vals = [0]
            first_diffs = list(diff[0] for diff in diffs)[:-1]
            first_diffs.reverse()
            for value in first_diffs:
                vals.append(value - vals[-1])

            interpolated_sum += vals[-1]

    return interpolated_sum


if __name__ == "__main__":
    print(part_1())
    print(part_2())
