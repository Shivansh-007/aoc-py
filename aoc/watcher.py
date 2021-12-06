import inspect
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from rich import print
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler

from aoc.constants import EXAMPLE_ANSWERS_FILE, ROOT, SUBMISSIONS_FILE


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
            solution, part = event.part_two, "2"
        else:
            print("[green]✅ Both are submitted :D[/]")
            exit()

    example_answers_file = Path(ROOT, f"{event.year}", EXAMPLE_ANSWERS_FILE)
    eg_answers = json.loads(example_answers_file.read_text())
    test_data, test_data_answer = eg_answers[event.day]["input"], eg_answers[event.day][part]

    if (sol_return := str(solution(test_data))) == test_data_answer:
        print(f"[green]✅ Successfully ran day {event.day} part {part} tests![/]")

        from aoc import submit
        submit(event, part, solution)
        check_puzzle(event)
    else:
        print(f"[red]❌ Testing of day {event.day} part {part} failed! Please try again. Here's the output:[/]")
        print(f"\t[green]Expected: {test_data_answer}")
        print(f"\t[red]Recieved: {sol_return}")
        return

class ModificationWatcher(FileSystemEventHandler):
    def __init__(self, caller_puzzle: Path):
        self.last_modified = datetime.now()
        self.caller_puzzle = caller_puzzle

        self.day = str(int(self.caller_puzzle.parent.name))
        self.year = self.caller_puzzle.parent.parent.name

        self.part_one, self.part_two, self.data = None, None, None
        self.get_p1_p2()

    def get_p1_p2(self):
        import sys
        sys.path.append(str(self.caller_puzzle.parent))

        from solution import data, part_one, part_two
        self.part_one, self.part_two, self.data = part_one, part_two, data

    def on_modified(self, event: FileSystemEvent):
        # On Linux and inside the container, it will double report file change so 
        # this prevents that from happening.
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()

        self.get_p1_p2()
        clear_screen()
        check_puzzle(self)


def watch():
    frame = inspect.stack()[1]
    caller_puzzle = Path(frame[0].f_code.co_filename)

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
