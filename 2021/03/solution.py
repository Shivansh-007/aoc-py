from collections import Counter

import aoc
from aoc.utils import AoCInput


def parse_data(raw):
    return AoCInput.get_lines(raw)


def part_one(raw):
    data = parse_data(raw)

    counted = [Counter(l) for l in zip(*data)]
    gamma = "".join(col.most_common()[0][0] for col in counted)
    epsilon = "".join(col.most_common()[-1][0] for col in counted)

    return int(gamma, base=2) * int(epsilon, base=2)


def part_two(raw):
    data = parse_data(raw)

    def oxy_gen(lines):
        for i in range(12):
            counted = [Counter(l) for l in zip(*lines)]
            # If 0 and 1 are equally common, keep values with a 1 in the position being considered.
            mc_bit = "1" if counted[i]["0"] == counted[i]["1"] else counted[i].most_common()[0][0]
            lines = [line for line in lines if line[i] == mc_bit]
        return int(lines[0], 2)

    def co2_scrub(lines):
        for i in range(12):
            counted = [Counter(l) for l in zip(*lines)]
            # If 0 and 1 are equally common, keep values with a 0 in the position being considered.
            lc_bit = "0" if counted[i]["0"] == counted[i]["1"] else counted[i].most_common()[-1][0]
            lines = [line for line in lines if line[i] == lc_bit]
        return int(lines[0], 2)

    return oxy_gen(data.copy()) * co2_scrub(data.copy())


if __name__ == "__main__":
    aoc.watch()
