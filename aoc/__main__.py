import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union

import bs4
import click
import httpx
from rich import print

from aoc import get_problem_examples
from aoc.constants import AOC_SESSION_COOKIE, EST, EXAMPLE_ANSWERS_FILE, ROOT, TEMPLATE_FILE

TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("second", 1),
)
SECONDS_DAY = 86400  # 60 * 60 * 24


def _human_time_duration(seconds):
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


def _time_left_till_problem(day: int, year: int) -> Union[tuple[datetime, timedelta], bool]:
    """Calculate the amount of time left until midnight EST/UTC-5."""
    # Change all time properties back to 00:00
    problem_midnight = datetime.now(tz=EST).replace(
        year=year, day=day, microsecond=0, second=0, minute=0, hour=0
    )

    return problem_midnight - datetime.now(tz=EST)


@click.group()
def cli():
    pass


@cli.command(name="setup")
@click.argument("year", nargs=1, type=int, metavar="YEAR...")
@click.pass_context
def setup_aoc_year(ctx: click.Context, year: int) -> None:
    """Setup AoC for year <year.>"""
    new_dir = Path(ROOT, f"{year}")
    if new_dir.exists():
        print(f"[red]Looks like AoC is already setup for year [blue]{year}[/], good luck![/]")
    else:
        new_dir.mkdir()
        print(f"All done! ✨ 🍰 ✨ Good luck on AoC {year} journey!")


@cli.command(name="start")
@click.option(
    "-d",
    "--day",
    default=datetime.now().day,
    type=click.IntRange(1, 25),
)
@click.option(
    "-y",
    "--year",
    default=datetime.now().year,
    type=int,
)
@click.option("-W", "--wait", is_flag=True, default=True, type=bool)
@click.pass_context
def start_aoc_day(ctx, day: int, year: int, wait: bool) -> None:
    time_left = _time_left_till_problem(day, year).total_seconds() if wait else -1

    if time_left > 0:
        if time_left > SECONDS_DAY:
            print(f"[yellow]🕔🚀🕤 You are going too fast, you just skipped day {day - 1} of Aoc!")
            return

        # As a safe guard, the sleep duration is padded with 0.1 second to make sure we wake up after midnight.
        sleep_seconds = time_left + 0.1
        print(
            f"[blue italic]Sleeping for {_human_time_duration(sleep_seconds)} until the next AoC puzzle :wave:[/]"
        )
        time.sleep(sleep_seconds)

    day_dir = Path(ROOT, f"{year}", f"{day:02}")
    if day_dir.exists():
        print(
            f"[red]Directory for day {day} is already setup at [blue]{day_dir.relative_to(Path.cwd().parent)}[/]"
        )
        return

    if AOC_SESSION_COOKIE is None:
        print(f"[red][bold]AOC_SESSION_COOKIE[/bold] not found in environment variables![/]")
        return

    problem_input = httpx.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        cookies={"session": AOC_SESSION_COOKIE},
    )

    if not problem_input.is_success:
        print(
            f"[bold red]Unexpected response [blue]'{problem_input.status_code}'[/blue] "
            f"while fetching problem input with URL <[blue]{problem_input.url}[/]>"
        )
        return

    day_dir.mkdir()

    input_file = Path(day_dir, "input.txt")
    input_file.write_text(problem_input.text)

    # Get problem example input and its answers for writing tests :D
    example_answers_file = Path(ROOT, f"{year}", EXAMPLE_ANSWERS_FILE)
    problem = httpx.get(
        f"https://adventofcode.com/{year}/day/{day}",
        cookies={"session": AOC_SESSION_COOKIE},
    )
    test_input, answer = get_problem_examples(problem)
    eg_answers = json.loads(example_answers_file.read_text())
    # Just write the part 1 answer has we have not finished it yet, so we won't be having the inputs :(
    eg_answers.setdefault(day, {"1": "", "2": ""})["1"] = answer
    eg_answers[day]["input"] = test_input
    example_answers_file.write_text(json.dumps(eg_answers, indent=4))

    # Make copy of solution template for the puzzle
    solution = Path(day_dir, "solution.py")
    solution.write_text(TEMPLATE_FILE.format(input_file=input_file.relative_to(ROOT), day=day))

    print("All done! ✨ 🍰 ✨ Good luck!")


main_cli = click.CommandCollection(sources=[cli])

if __name__ == "__main__":
    main_cli()
