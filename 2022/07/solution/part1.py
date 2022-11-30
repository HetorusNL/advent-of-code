from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")

    def get_result(self) -> str:
        result = 42
        return f"the result of part 1 is: {result}"
