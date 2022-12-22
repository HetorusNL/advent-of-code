from pathlib import Path

from solution.grid_2d import Grid2D


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.removesuffix("\n") for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        grid = Grid2D(self.lines)
        grid.perform_instructions()
        self.password = grid.get_password()

    def get_result(self) -> str:
        return f"the final 2D grid password is: {self.password}"
