from pathlib import Path

from solution.pos import Pos
from solution.trail2 import Trail


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.grid: dict[int, dict[int, str]] = {}
        for row, line in enumerate(self.lines):
            self.grid[row] = {}
            for col, char in enumerate(line):
                self.grid[row][col] = char
        start_pos = Pos(0, self.lines[0].index("."))
        end_pos = Pos(len(self.lines) - 1, self.lines[-1].index("."))

        trail = Trail(start_pos, self.grid)
        self.result = trail.run(start_pos, end_pos)

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
