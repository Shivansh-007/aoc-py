import statistics

import aoc
from aoc.utils import AoCInput


def parse_data(raw):
    data = AoCInput.get_lines(raw)[0]
    data = list(map(int, data.split(",")))
    return sorted(data)


def part_one(raw):
    data = parse_data(raw)
    median = int(statistics.median(data))
    return sum(abs(x - median) for x in data)


def part_two(raw):
    data = parse_data(raw)
    ap_sum = lambda i: i * (i + 1) // 2
    return min(sum(ap_sum(abs(m - x)) for x in data) for m in range(data[0], data[-1]))


if __name__ == "__main__":
    aoc.watch()
