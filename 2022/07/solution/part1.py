from pathlib import Path

from solution.log_interpreter import LogInterpreter


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        log_interpreter = LogInterpreter()
        for line in self.lines:
            log_interpreter.interpret_line(line)

        # calculate the sum of the directory sizes of directories smaller than 100k
        directory_sizes = log_interpreter.filesystem_size.values()
        self.directory_sizes_below_100k = sum(value for value in directory_sizes if value < 100_000)

    def get_result(self) -> str:
        return f"the sum of the directory sizes below 100k is: {self.directory_sizes_below_100k}"
