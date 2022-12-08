from pathlib import Path

from solution.grid import Grid


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        grid = Grid(self.lines)
        self.scenic_score = grid.get_max_scenic_score()

    def get_result(self) -> str:
        return f"the maximum scenic score of the grid is: {self.scenic_score}"
