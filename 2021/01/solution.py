from itertools import pairwise

from more_itertools import triplewise

import aoc
from aoc.utils import AoCInput


def parse_data(raw):
    return AoCInput.get_ints(raw)


def part_one(raw):
    data = parse_data(raw)
    return sum(y > x for x, y in pairwise(data))


def part_two(raw):
    data = parse_data(raw)
    return sum(y > x for x, y in pairwise(sum(i) for i in triplewise(data)))


if __name__ == "__main__":
    aoc.watch()
