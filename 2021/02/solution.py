import aoc
from aoc.utils import AoCInput


def parse_data(raw):
    data = AoCInput.get_lines(raw)
    return [l.split(" ") for l in data]


def part_one(raw):
    data = parse_data(raw)
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


def part_two(raw):
    data = parse_data(raw)
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


if __name__ == "__main__":
    aoc.watch()
