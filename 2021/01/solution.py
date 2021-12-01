from itertools import pairwise

from more_itertools import triplewise

import aoc
from aoc.utils import extract_ints


def parse_data():
    with open("2021/01/input.txt") as f:
        data = f.read()

    return list(extract_ints(data))


data = parse_data()


def part_one():
   return sum(y > x for x, y in pairwise(data))


def part_two():
   return sum(y > x for x, y in pairwise(sum(i) for i in triplewise(data))) 

aoc.submit(1, 2021, part_one)
aoc.submit(1, 2021, part_two)
