import os
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv(override=True)

if "--test" in sys.argv:
    AOC_SESSION_COOKIE = os.environ.get("TEST_AOC_SESSION_COOKIE")
else:
    AOC_SESSION_COOKIE = os.environ.get("AOC_SESSION_COOKIE")

ROOT = Path(__file__).parent.parent
SUBMISSIONS_FILE = "submissions.json"
EXAMPLE_ANSWERS_FILE = "example_answers.json"
URL = "https://adventofcode.com/{year}/day/{day}"
EST = ZoneInfo("America/New_York")

with open("aoc/template.txt") as f:
    TEMPLATE_FILE = f.read()
