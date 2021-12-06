<p align="center"><img src="./2021/aoc21.png"></p>

**2020 | [2021](https://github.com/Shivansh-007/aoc-py/tree/main/2021)**

Here lies my python solutions to [Advent of Code 2021](https://adventofcode.com/), an Advent calendar full of programming puzzles from December 1st all the way to Christmas. I don't have any particularly ambitious goals, but I am trying to write the solutions using idiomatic code. In particular, it should not be possible for any input to cause one of the solutions to panic.

### Installation
```bash
$ git clone https://github.com/Shivansh-007/aoc-py
$ cd aoc-py
$ poetry install
```

### Usage

- **Setup a template for a day's puzzle**
    ```bash
    $ python -m aoc start --day {day}
    ```

- **Open the watch shell**
    
    This will try to verify the completition of the puzzle solution by running the test examples scrapped for the puzzle page. If the tests are successfuly, it will go ahead and submit the answer to adventofcode.com, depending on the result you either continue with part 2 or fix your part 1 solution. The samething repeates with part 2.

    The watch shell is semi-pretty with help of rich :D 
    ```bash
    $ python -m 2021.{day}.solution
    ```


