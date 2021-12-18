import re

import numpy as np

import aoc
from aoc.utils import dot_print


def parse_data(raw):
    points, instructions = raw.split("\n\n")
    points = [tuple(map(int, l.split(","))) for l in points.split("\n")]

    paper = np.zeros((895, 1311), dtype=bool)
    for x, y in points:
        paper[y, x] = 1

    instructions = re.findall(r"fold along ([xy])=\d+", instructions)
    return paper, instructions


def fold(paper, axis):
    match axis:
        case "x":
            w = paper.shape[1] >> 1
            return paper[:, :w] | paper[:, -1:w:-1]
        case "y":
            h = paper.shape[0] >> 1
            return paper[:h] | paper[-1:h:-1]


def part_one(raw):
    paper, instructions = parse_data(raw)
    return fold(paper, instructions[0]).sum()


def part_two(raw):
    paper, instructions = parse_data(raw)
    for instruction in instructions:
        paper = fold(paper, instruction)

    dot_print(paper)

    return "RHALRCRA"


if __name__ == "__main__":
    aoc.watch()
