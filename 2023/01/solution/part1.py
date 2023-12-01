from pathlib import Path
import re


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        values = []
        for line in self.lines:
            start = re.search(r"[0-9]", line)
            assert start
            end = re.search(r"[0-9]", line[::-1])
            assert end
            values.append(int(start.group(0) + end.group(0)))
        self.result = sum(values)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
