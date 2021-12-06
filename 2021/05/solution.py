import re
from collections import Counter

import aoc
from aoc.utils import AoCInput


def parse_data(raw):
    return AoCInput.get_lines(raw)


def part_one(raw):
    data = parse_data(raw)
    all_coors = []

    for line in data:
        x1, y1, x2, y2 = map(int, re.findall(r"(\d+),(\d+) -> (\d+),(\d+)", line)[0])
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                all_coors.append((x1, y))
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                all_coors.append((x, y1))

    positions = Counter(all_coors)
    return len([coor for coor, n in positions.items() if n >= 2])


def part_two(raw):
    data = parse_data(raw)
    all_coors = []

    for line in data:
        x1, y1, x2, y2 = map(int, re.findall(r"(\d+),(\d+) -> (\d+),(\d+)", line)[0])
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                all_coors.append((x1, y))
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                all_coors.append((x, y1))
        else:
            dx, dy = [1, -1][x1 > x2], [1, -1][y1 > y2]
            x, y = x1, y1

            while True:
                all_coors.append((x, y))
                if (x, y) == (x2, y2):
                    break
                x += dx
                y += dy

    positions = Counter(all_coors)
    return len([coor for coor, n in positions.items() if n >= 2])


if __name__ == "__main__":
    aoc.watch()
