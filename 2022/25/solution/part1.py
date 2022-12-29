from pathlib import Path

from solution.snafu import SNAFU


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        fuel_sum = sum(SNAFU.from_snafu(line) for line in self.lines)
        self.snafu_sum = SNAFU.to_snafu(fuel_sum)

    def get_result(self) -> str:
        return f"the SNAFU number to enter in Bob's console is: {self.snafu_sum}"
