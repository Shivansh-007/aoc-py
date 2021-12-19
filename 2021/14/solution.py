from collections import Counter
from more_itertools import pairwise

import aoc


def parse_data(raw):
    polymer, rules = raw.split("\n\n")

    return (
        polymer,
        {
            (a, b): c for (a, b), c in [r.split(" -> ") for r in rules.split("\n")]
        },
    )

def n_iteractions(polymer, steps, n):
    counter = Counter(pairwise(polymer))
    
    for _ in range(n):
        new_counter = Counter()

        for p, count in counter.copy().items():
            c = steps[p]
            new_counter[(p[0], c)] += count
            new_counter[(c, p[1])] += count

        counter = new_counter

    single = Counter()
    for (a, _), count in counter.items():
        single[a] += count
    single[polymer[-1]] += 1

    return single.most_common()[0][1] - single.most_common()[-1][1]


def part_one(raw):
    data = parse_data(raw)
    return n_iteractions(data[0], data[1], 10)


def part_two(raw):
    data = parse_data(raw)
    return n_iteractions(data[0], data[1], 40)

if __name__ == "__main__":
    aoc.watch()