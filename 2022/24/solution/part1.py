from pathlib import Path

from solution.grid import Grid


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        grid = Grid(self.lines)
        iteration = 0
        while iteration := iteration + 1:
            grid.update()
            if grid.goal_reached():
                self.iterations = iteration
                break

    def get_result(self) -> str:
        return f"goal reached after iterations: {self.iterations}"
