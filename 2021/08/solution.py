from itertools import permutations

import aoc
from aoc.utils import AoCInput


def parse_data(raw):
    data = AoCInput.get_lines(raw)
    data = [tuple(map(str.strip, line.split("|"))) for line in data]
    return data


def part_one(raw):
    data = parse_data(raw)
    count = 0

    for line in data:
        output = line[1].split()
        count += sum(len(x) in (2, 3, 4, 7) for x in output)

    return count


def part_two(raw):
    data = parse_data(raw)
    ALL = "abcdefg"
    CORRECT_MAP = {
        "abcefg": 0,
        "cf": 1,
        "acdeg": 2,
        "acdfg": 3,
        "bcdf": 4,
        "abdfg": 5,
        "abdefg": 6,
        "acf": 7,
        "abcdefg": 8,
        "abcdfg": 9,
    }
    join_map = lambda map, string: "".join(sorted([map[i] for i in string]))

    ans = 0
    for ld, numbers in data:
        ld, numbers = ld.split(), numbers.split()
        for perm in permutations(ALL):
            mapping = {x: ALL[i] for i, x in enumerate(perm)}
            if all(join_map(mapping, w) in CORRECT_MAP for w in ld):
                digits = [
                    [CORRECT_MAP[x] for x in CORRECT_MAP if x == join_map(mapping, unmapped)][0]
                    for unmapped in numbers
                ]
                ans += int("".join(map(str, digits)))

    return ans


if __name__ == "__main__":
    aoc.watch()
