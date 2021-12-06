import inspect
import json
import os
import sys
import time
from datetime import datetime, timedelta
from email import message
from pathlib import Path

import httpx
from rich import print
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from aoc.constants import AOC_SESSION_COOKIE, EXAMPLE_ANSWERS_FILE, ROOT, SUBMISSIONS_FILE


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def check_puzzle(event: "ModificationWatcher"):
    # If this part is already submitted, we can close the observer
    submissions_file = Path(ROOT, f"{event.year}", SUBMISSIONS_FILE)
    submissions = json.loads(submissions_file.read_text())

    try:
        submissions[event.day]["1"]["solution"]
    except KeyError:
        solution, part = event.part_one, "1"
    else:
        try:
            submissions[event.day]["2"]["solution"]
        except KeyError:
            from aoc import get_problem_examples

            example_answers_file = Path(ROOT, f"{event.year}", EXAMPLE_ANSWERS_FILE)
            problem = httpx.get(
                f"https://adventofcode.com/{event.year}/day/{event.day}",
                cookies={"session": AOC_SESSION_COOKIE},
            )
            _, answer = get_problem_examples(problem)
            eg_answers = json.loads(example_answers_file.read_text())
            eg_answers[event.day]["2"] = answer
            example_answers_file.write_text(json.dumps(eg_answers, indent=4))

            solution, part = event.part_two, "2"
        else:
            print("[green]✅ Both are submitted :D[/]")
            exit()

    print(f"{solution} of {part}...")

    example_answers_file = Path(ROOT, f"{event.year}", EXAMPLE_ANSWERS_FILE)
    eg_answers = json.loads(example_answers_file.read_text())
    test_data, test_data_answer = eg_answers[event.day]["input"], eg_answers[event.day][part]

    if (sol_return := str(solution(test_data))) == test_data_answer:
        print(f"[green]✅ Successfully ran day {event.day} part {part} tests![/]")

        from aoc import submit

        submit(event, part, solution)

        check_puzzle(event)
    else:
        print(
            message := f"[red]❌ Testing of day {event.day} part {part} failed! Please try again. Here's the output:[/]"
        )
        print(f"\t[green]Expected: {test_data_answer}")
        print(f"\t[red]Recieved: {sol_return}")
        print(len(message) * "=")
        return


class ModificationWatcher(FileSystemEventHandler):
    def __init__(self, caller_puzzle: Path):
        self.last_modified = datetime.now()
        self.caller_puzzle = caller_puzzle

        self.day = str(int(self.caller_puzzle.parent.name))
        self.year = self.caller_puzzle.parent.parent.name

        sys.path.append(str(self.caller_puzzle.parent))

        self.part_one, self.part_two, self.data = None, None, None
        self.get_p1_p2()

        self.data = Path(caller_puzzle.parent, "input.txt").read_text()

    def get_p1_p2(self):
        print("imported...")
        from solution import part_one, part_two

        print("imported...")
        self.part_one, self.part_two = part_one, part_two

    def on_modified(self, event: FileSystemEvent):
        print("Modified")
        # On Linux and inside the container, it will double report file change so
        # this prevents that from happening.
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            print("returning...")
            return
        else:
            self.last_modified = datetime.now()

        self.get_p1_p2()
        clear_screen()
        print("checking...")
        check_puzzle(self)


def watch():
    frame = inspect.stack()[1]
    caller_puzzle = Path(frame[0].f_code.co_filename)
    print(caller_puzzle.parent)

    event_handler = ModificationWatcher(caller_puzzle)
    observer = Observer()
    observer.schedule(event_handler, path=caller_puzzle.parent, recursive=False)
    observer.start()

    try:
        check_puzzle(event_handler)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        exit(0)
