from itertools import pairwise

from more_itertools import triplewise

import aoc
from aoc.utils import AoCInput

data = AoCInput("2021/01/input.txt").get_ints()


def part_one():
    return sum(y > x for x, y in pairwise(data))


def part_two():
    return sum(y > x for x, y in pairwise(sum(i) for i in triplewise(data)))


aoc.submit(part_one)
aoc.submit(part_two)
