import inspect
import json
from operator import sub
import os
from datetime import datetime, timedelta
from pathlib import Path
import time
import typing

from rich import print
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler

from aoc.constants import EXAMPLE_ANSWERS_FILE, ROOT, SUBMISSIONS_FILE

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_puzzle(part_one: typing.Callable, part_two: typing.Callable, data: typing.Any, submission_file: typing.Sequence[Path]):
    # If this part is already submitted, we can close the observer
    day, year = str(int(submission_file[0].name)), submission_file[1].name
    submissions_file = Path(ROOT, f"{year}", SUBMISSIONS_FILE)
    submissions = json.loads(submissions_file.read_text())

    try:
        submissions[day]["1"]["solution"]
    except KeyError:
        solution, part  = part_one, "1"
    else:
        try:
            submissions[day]["2"]["solution"]
        except KeyError:
            solution, part = part_two, "2"
        else:
            print("Both are submitted :D")
            exit()

    example_answers_file = Path(ROOT, f"{year}", EXAMPLE_ANSWERS_FILE)
    eg_answers = json.loads(example_answers_file.read_text())
    test_data, test_data_answer = eg_answers[day]["input"], eg_answers[day][part]

    if (sol_return := str(solution(test_data))) == test_data_answer:
        print(f"[green]✅ Successfully ran day {day} part {part} tests![/]")
        from aoc import submit
        submit(solution, part, data, submission_file)
        check_puzzle(part_two, part_two, data, submission_file)
    else:
        print(f"[red]❌ Testing of day {day} part {part} failed! Please try again. Here's the output:[/]")
        print(f"\t[green]Expected: {test_data_answer}")
        print(f"\t[red]Recieved: {sol_return}")
        return


class ModificationWatcher(FileSystemEventHandler):
    def __init__(self, part_one: typing.Callable, part_two: typing.Callable, data: typing.Any, submission_file: typing.Sequence[Path]):
        self.last_modified = datetime.now()
        self.data = data
        self.submission_file = submission_file

        self.part_one = part_one
        self.part_two = part_two

    def reload_functions(self):
        # HACK Please don't do this
        solution = Path(self.submission_file[0], "solution.py")
        with open(solution) as f:
            code = compile(f.read(), solution, 'exec')
            exec(code, globals(), locals())

        print(globals())

    def on_modified(self, event: FileSystemEvent):
        # On Linux and inside the container, it will double report file change so 
        # this prevents that from happening.
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()

        self.reload_functions()
        clear_screen()
        check_puzzle(self.part_one, self.part_two, self.data, self.submission_file)


def watch(part_one: typing.Callable, part_two: typing.Callable, data: typing.Any):
    frame = inspect.stack()[1]
    submission_file = Path(frame[0].f_code.co_filename).parents

    event_handler = ModificationWatcher(part_one, part_two, data, submission_file)
    observer = Observer()
    observer.schedule(event_handler, path=submission_file[0], recursive=False)
    observer.start()

    try:
        check_puzzle(part_one, part_two, data, submission_file)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        exit(0)
