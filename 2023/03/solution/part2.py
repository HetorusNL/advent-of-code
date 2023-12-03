from pathlib import Path

from solution.grid import Grid


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        grid = Grid(self.lines)
        gears = grid.get_gears()
        self.result = sum(gear.value() for gear in gears)

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
