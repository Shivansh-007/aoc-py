import aoc
from aoc.utils import AoCInput

data = AoCInput("2021/02/input.txt").get_lines()
data = [l.split(" ") for l in data]


def part_one():
    depth = 0
    horizontal = 0
    for (command, x) in data:
        match command:
            case "forward":
                horizontal += int(x)
            case "down":
                depth += int(x)
            case "up":
                depth -= int(x)
    return depth * horizontal


def part_two():
    aim = 0
    depth = 0
    horizontal = 0

    for (command, x) in data:
        match command:
            case "forward":
                horizontal += int(x)
                depth += int(x) * aim
            case "down":
                aim += int(x)
            case "up":
                aim -= int(x)
    return depth * horizontal


aoc.submit(part_one)
aoc.submit(part_two)
