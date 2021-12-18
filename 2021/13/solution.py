import re
from pathlib import Path

from rich import print


def parse_data(raw):
    points, instructions = raw.split("\n\n")
    points = [tuple(map(int, l.split(","))) for l in points.split("\n")]

    max_x, max_y = max(points, key=lambda p: p[0])[0] + 1, max(points, key=lambda p: p[1])[1] + 1
    paper = [["."] * max_x for _ in range(max_y)]
    for x, y in points:
        paper[y][x] = "#"

    instructions = re.findall(r"fold along ([xy])=\d+", instructions)
    return paper, instructions


def merge_array(a, b):
    return [b[i] if dot == "." else dot for i, dot in enumerate(a)]


def fold_paper(paper, vertical=False):
    folded = []

    if vertical:
        paper = list(map(list, zip(*paper)))

    while True:
        if len(paper) == 1:
            return folded
        a, b = paper.pop(0), paper.pop(-1)
        folded.append(merge_array(a, b))


def part_one(raw):
    paper, instructions = parse_data(raw)
    folded = fold_paper(paper, instructions[0] == "x")
    return sum(sum(dot == "#" for dot in dots) for dots in folded)


def part_two(raw):
    paper, instructions = parse_data(raw)

    for instruction in instructions:
        paper = fold_paper(paper, instruction == "x")

    return paper


print(part_two(Path("2021/13/input.txt").read_text()))
