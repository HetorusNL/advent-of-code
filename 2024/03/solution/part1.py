from pathlib import Path
import re


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        for line in self.lines:
            offset = 0
            while match := re.search(r"mul\((?P<left>[0-9]*),(?P<right>[0-9]*)\)", line[offset:]):
                offset += match.end()
                self.result += int(match.groupdict()["left"]) * int(match.groupdict()["right"])

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
