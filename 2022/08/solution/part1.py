from pathlib import Path

from solution.grid import Grid


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        grid = Grid(self.lines)
        self.viewable_trees = grid.get_viewable_trees()

    def get_result(self) -> str:
        return f"the number of viewable trees in the grid is: {self.viewable_trees}"
