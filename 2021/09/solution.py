from functools import reduce
from operator import mul

import aoc
from aoc.utils import AoCInput


def parse_data(raw):
    data = AoCInput.get_lines(raw)
    data = [list(map(int, list(line.strip()))) for line in data]
    return data


def lowest_coors(data):
    levels = []
    for line_id, line in enumerate(data):
        for i in range(len(line)):
            compare = []
            if i != 0:
                compare.append(line[i - 1])
            if i != len(line) - 1:
                compare.append(line[i + 1])
            if line_id != 0:
                compare.append(data[line_id - 1][i])
            if line_id != len(data) - 1:
                compare.append(data[line_id + 1][i])

            if all(x > line[i] for x in compare):
                levels.append((line_id, i))

    return levels


def part_one(raw):
    data = parse_data(raw)
    lowest = lowest_coors(data)
    levels = [data[row][col] for row, col in lowest]

    return sum(levels) + len(levels)


def part_two(raw):
    data = parse_data(raw)
    lowest = lowest_coors(data)

    def get_basin(x, y):
        basin = {(x, y)}
        basin |= follow_basin(x, y)
        return basin

    def follow_basin(x, y):
        basin = set()
        p1 = data[x][y]
        neighbours = {(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)}

        for n_x, n_y in neighbours:
            if any(p < 0 for p in (n_x, n_y)):
                continue
            try:
                p2 = data[n_x][n_y]
            except IndexError:
                continue

            if p2 > p1 and p2 != 9:
                basin.add((n_x, n_y))
                basin |= follow_basin(n_x, n_y)

        return basin

    return reduce(mul, sorted(len(get_basin(*coor)) for coor in lowest)[-3:], 1)


if __name__ == "__main__":
    aoc.watch()
