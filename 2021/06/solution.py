from collections import Counter

import aoc
from aoc.utils import AoCInput

raw = AoCInput("2021/06/input.txt").get_ints(r"(\d+)")
fish = Counter(raw)


def nfish(days):
    _fish = fish.copy()
    for i in range(days):
        _fish = Counter(
            {i: _fish[i + 1] for i in range(6)}
            | {
                # All '6's get set to '7' as '-1' is done from them
                # and the '0's because new lanterfishes were born :D
                6: _fish[0] + _fish[7],
                # All '7's get set to '8' as '-1' is done from them
                7: _fish[8],
                # All '0's get set to '8'
                8: _fish[0],
            }
        )

    return sum(_fish.values())


def part_one():
    return nfish(80)


def part_two():
    return nfish(256)


aoc.submit(part_one)
aoc.submit(part_two)
