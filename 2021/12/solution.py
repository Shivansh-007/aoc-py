from collections import defaultdict
from pathlib import Path

from aoc.utils import AoCInput


def parse_data(raw):
    data = AoCInput.get_lines(raw)
    graph = defaultdict(set)

    data = [line.split("-") for line in data]
    for a, b in data:
        graph[a].add(b)
        graph[b].add(a)

    return graph


def part_one(raw):
    graph = parse_data(raw)

    dfs_stack = [("start",)]
    total = 0

    while dfs_stack:
        cave_path = dfs_stack.pop()
        if cave_path[-1] == "end":
            total += 1
            continue

        for next_cave in graph[cave_path[-1]]:
            if next_cave.isupper() or next_cave not in cave_path:
                dfs_stack.append((*cave_path, next_cave))

    return total


def part_two(raw):
    graph = parse_data(raw)

    dfs_stack = [(("start",), False)]
    total = 0

    while dfs_stack:
        cave_path, twice = dfs_stack.pop()
        if cave_path[-1] == "end":
            total += 1
            continue

        for next_cave in graph[cave_path[-1]] - {"start"}:
            if next_cave not in cave_path or next_cave.isupper():
                dfs_stack.append(((*cave_path, next_cave), twice))
            elif not twice and cave_path.count(next_cave) == 1:
                dfs_stack.append(((*cave_path, next_cave), True))

    return total


print(part_one(Path("2021/12/input.txt").read_text()))
print(part_two(Path("2021/12/input.txt").read_text()))

# if __name__ == "__main__":
# aoc.watch()
