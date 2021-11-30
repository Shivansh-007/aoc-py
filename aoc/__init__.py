# Credit: https://github.com/salt-die/Advent-of-Code/tree/master/2021/aoc_helper

import json
import re
import time
import webbrowser
from pathlib import Path
from typing import Callable

import bs4
import httpx
from rich import print

from aoc.constants import AOC_SESSION_COOKIE, SUBMISSIONS_FILE, ROOT, URL

__all__ = (
    "submit",
)


def submit(day, year, solution: Callable):
    """Submit an AoC solution. Submissions are cached."""
    day = str(day)
    submissions_file = Path(ROOT, f"{year}", SUBMISSIONS_FILE)

    match solution.__name__:
        case "part_one":
            part = "1"
        case "part_two":
            part = "2"
        case _:
            print(f"[red]solution callable has bad name, [bold]{solution.__name__}[/]")
            return

    submissions = json.loads(submissions_file.read_text())
    current = submissions.setdefault(day, {"1": {}, "2": {}})[part]

    if "solution" in current:
        print(
            f"Day {day} part {part} has already been solved. "
            f"The solution was:\n{current['solution']}."
        )
        return

    solution = solution()
    if solution is None:
        return

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
            data={"level": part, "answer": solution}
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
