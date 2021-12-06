from collections import Counter

import aoc
from aoc.utils import AoCInput


def nfish(fish, days):
    for i in range(days):
        fish = Counter(
            {i: fish[i + 1] for i in range(6)}
            | {
                # All '6's get set to '7' as '-1' is done from them
                # and the '0's because new lanterfishes were born :D
                6: fish[0] + fish[7],
                # All '7's get set to '8' as '-1' is done from them
                7: fish[8],
                # All '0's get set to '8'
                8: fish[0],
            }
        )

    return sum(fish.values())


def parse_data(raw):
    raw = AoCInput().get_ints(raw, regexp=r"(\d+)")
    return Counter(raw)


def part_one(raw):
    fish = parse_data(raw)
    return nfish(fish, 80)


def part_two(raw):
    fish = parse_data(raw)
    return nfish(fish, 256)


if __name__ == "__main__":
    aoc.watch()
