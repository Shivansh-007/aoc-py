# Credit: https://github.com/salt-die/Advent-of-Code/tree/master/2021/aoc_helper

import inspect
import json
import re
import time
import typing
import webbrowser
from pathlib import Path
from typing import Callable

import bs4
import httpx
from rich import print

from aoc.constants import AOC_SESSION_COOKIE, ROOT, SUBMISSIONS_FILE, URL
from aoc.watcher import watch

__all__ = ("submit", "watch")


def _seconds_to_most_relevant_unit(s):
    s *= 1e6
    if s < 1000:
        return f"{s:.3f}µs"

    s /= 1000
    if s < 1000:
        return f"{s:.3f}ms"

    s /= 1000
    if s < 60:
        return f"{s:.3f}s"

    s /= 60
    return f"{int(s):d}m {s/60%60:.3f}s"


def submit(solution: Callable, part: str, data: typing.Any, submission_file: typing.Sequence[Path]):
    """Submit an AoC solution. Submissions are cached."""
    day, year = submission_file[0].name, submission_file[1].name
    day = str(int(day))

    submissions_file = Path(ROOT, f"{year}", SUBMISSIONS_FILE)

    submissions = json.loads(submissions_file.read_text())
    current = submissions.setdefault(day, {"1": {}, "2": {}})[part]

    if "solution" in current:
        print(f"Day {day} part {part} has already been solved. " f"The solution was:\n{current['solution']}.")
        return

    start_wall, start_cpu = time.perf_counter(), time.process_time()
    solution = solution(data)
    now_wall, now_cpu = time.perf_counter(), time.process_time()

    if solution is None:
        return

    dt_wall = _seconds_to_most_relevant_unit(now_wall - start_wall)
    dt_cpu = _seconds_to_most_relevant_unit(now_cpu - start_cpu)

    print(f"Timer [magenta]{year}.{day}.part_{part}[/]: [blue]{dt_wall}[/] wall, [blue]{dt_cpu}[/] CPU")

    solution = str(solution)

    if solution in current:
        print(f"Solution {solution} to part {part} has already been submitted, response was:")
        _pretty_print(current[solution])
        return

    while True:
        print(f"Submitting [green bold]{solution}[/] as solution to part {part}...")
        response = httpx.post(
            url=URL.format(day=day, year=year) + "/answer",
            cookies={"session": AOC_SESSION_COOKIE},
            data={"level": part, "answer": solution},
        )

        if response.is_error:
            print(
                f"[bold red]Unexpected response [blue]'{response.status_code}'[/blue] "
                f"while submission solution on URL <[blue]{response.url}[/]>"
            )
            return

        message = bs4.BeautifulSoup(response.text, "html.parser").article.text
        _pretty_print(message)

        if message[4] == "g":  # "You gave an answer too recently"
            minutes, seconds = re.search(r"(?:(\d+)m )?(\d+)s", message).groups()

            timeout = 60 * int(minutes or 0) + int(seconds)
            print(f"Waiting [blue]{timeout}[/] seconds to retry...")
            time.sleep(timeout)
        else:
            break

    if message[7] == "t":  # "That's the right answer! ..."
        current["solution"] = solution

        if part == "1":
            webbrowser.open(str(response.url))  # View part 2 in browser

    current[solution] = message
    submissions_file.write_text(json.dumps(submissions, indent=4))


def _pretty_print(message):
    match message[7]:
        case "t":
            # "That's the right answer! ..."
            colour = "green"
        case "'" | "e":
            # "You don't seem to be solving the right level. ..."
            # "You gave an answer too recently; you have to wait ..."
            colour = "yellow"
        case "n":
            # "That's not the right answer. If you're stuck, ..."
            colour = "red"
        case _:
            print(f"[bold red]Unexpected message:[/]\n{message}")
            return

    print(f"[bold {colour}]{message}[/]")
