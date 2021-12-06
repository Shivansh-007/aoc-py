import re
from collections import Counter

import aoc
from aoc.utils import AoCInput

data = AoCInput("2021/05/input.txt").get_lines()


def get_coors(x1, y1, x2, y2):
    if x1 == x2:
        return [(x1, int(i)) for i in range(y1, y2 + 1, int(abs(y2 - y1) / (y2 - y1)))]
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    slope = (y2 - y1) // (x2 - x1)
    line = []
    i = 0
    while x1 + i <= x2:
        i += 1
        line.append((x1 + i, y1 + slope * i))
    return line


def part_one():
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


def part_two():
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


aoc.submit(part_one)
aoc.submit(part_two)
