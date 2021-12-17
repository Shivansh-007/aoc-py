import aoc
from aoc.utils import AoCInput


def parse_data(raw):
    return AoCInput.get_lines(raw)


def part_one(raw):
    data = parse_data(raw)
    ans = 0

    points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    maps = {"(": ")", "[": "]", "{": "}", "<": ">"}

    for line in data:
        stack = []
        for bracket in line:
            if bracket in maps.keys():
                stack.append(bracket)
            elif bracket == maps[stack[-1]]:
                stack.pop()
            else:
                ans += points[bracket]
                break
    return ans


def part_two(raw):
    data = parse_data(raw)
    ans = []
    points = {")": 1, "]": 2, "}": 3, ">": 4}
    maps = {"(": ")", "[": "]", "{": "}", "<": ">"}

    for line in data:
        line_points = 0
        stack = []
        for bracket in line:
            if bracket in maps:
                stack.append(bracket)
            elif bracket == maps[stack[-1]]:
                stack.pop()
            else:
                break
        else:
            for bracket in reversed(stack):
                line_points = (line_points * 5) + points[maps[bracket]]
            ans.append(line_points)

    ans.sort()
    return ans[len(ans) // 2]


if __name__ == "__main__":
    aoc.watch()
