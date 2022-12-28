from pathlib import Path

from solution.grid import Grid


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        grid = Grid(self.lines)
        for _ in range(10):
            grid.do_round()
        self.num_elves = grid.num_elves()

    def get_result(self) -> str:
        return f"rectangle containing all elves, contains num empty ground tiles: {self.num_elves}"
