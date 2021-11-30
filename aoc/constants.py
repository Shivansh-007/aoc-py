import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

AOC_SESSION_COOKIE = os.environ.get("AOC_SESSION_COOKIE")
ROOT = Path(__file__).parent.parent
SUBMISSIONS_FILE = "submissions.json"
URL = "https://adventofcode.com/{year}/day/{day}"

with open("aoc/template.txt") as f:
    TEMPLATE_FILE = f.read()
