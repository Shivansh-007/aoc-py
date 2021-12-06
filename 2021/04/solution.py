from functools import reduce
from operator import add

from more_itertools import grouper

import aoc
from aoc.utils import AoCInput

data = AoCInput("2021/04/input.txt").get_lines()
numbers = [int(x) for x in data[0].split(",")]
boards = list(map(lambda b: [list(map(int, l.split())) for l in b[:-1]], grouper(data[2:], 6)))


def check_board_win(board, marked) -> bool:
    board = [["-1" if r in marked else r for r in row] for row in board]
    col_board = list(map(list, zip(*board)))

    return any(all(i == "-1" for i in row) for row in board) or any(
        all(i == "-1" for i in col) for col in col_board
    )


def part_one():
    marked = set()
    for n in numbers:
        marked.add(n)
        _boards = [board for board in boards if check_board_win(board, marked)]

        if _boards:
            return sum(set(reduce(add, _boards[0])) - marked) * n


def part_two():
    marked = set()
    _boards = boards.copy()
    for n in numbers:
        marked.add(n)
        if len(_boards) == 1:
            if check_board_win(_boards[0], marked):
                break
        else:
            _boards = [board for board in _boards if not check_board_win(board, marked)]

    return sum(set(reduce(add, _boards[0])) - marked) * n


aoc.submit(part_one)
aoc.submit(part_two)
