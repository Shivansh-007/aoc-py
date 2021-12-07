import re
from collections import Counter

import aoc
from aoc.utils import AoCInput, erange


def parse_data(raw):
    return AoCInput.get_lines(raw)


def part_one(raw):
    data = parse_data(raw)
    all_coors = []

    for line in data:
        x1, y1, x2, y2 = map(int, re.findall(r"(\d+),(\d+) -> (\d+),(\d+)", line)[0])
        if x1 == x2:
            all_coors += list(zip([x1] * (abs(y1 - y2) + 1), erange(y1, y2)))
        elif y1 == y2:
            all_coors += list(zip(erange(x1, x2), [y1] * (abs(x1 - x2) + 1)))

    positions = Counter(all_coors)
    return len([coor for coor, n in positions.items() if n >= 2])


def part_two(raw):
    data = parse_data(raw)
    all_coors = []

    for line in data:
        x1, y1, x2, y2 = map(int, re.findall(r"(\d+),(\d+) -> (\d+),(\d+)", line)[0])
        if x1 == x2:
            all_coors += list(zip([x1] * (abs(y1 - y2) + 1), erange(y1, y2)))
        elif y1 == y2:
            all_coors += list(zip(erange(x1, x2), [y1] * (abs(x1 - x2) + 1)))
        else:
            all_coors += list(zip(erange(x1, x2), erange(y1, y2)))

    positions = Counter(all_coors)
    return len([coor for coor, n in positions.items() if n >= 2])


if __name__ == "__main__":
    aoc.watch()
