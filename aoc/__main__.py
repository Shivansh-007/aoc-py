from datetime import datetime
from pathlib import Path

import click
import httpx
from rich import print

from aoc.constants import AOC_SESSION_COOKIE, ROOT, TEMPLATE_FILE


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
    "--day",
    default=datetime.now().day,
    type=click.IntRange(1, 25),
)
@click.option(
    "--year",
    default=datetime.now().year,
    type=int,
)
@click.pass_context
def start_aoc_day(ctx, day: int, year: int) -> None:
    day_dir = Path(ROOT, f"{year}", f"{day:02}")
    if day_dir.exists():
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

    solution = Path(day_dir, "solution.py")
    solution.write_text(TEMPLATE_FILE.format(input_file=input_file.relative_to(ROOT), day=day))
    print(f"All done! ✨ 🍰 ✨ Good luck!")


main_cli = click.CommandCollection(sources=[cli])

if __name__ == "__main__":
    main_cli()
