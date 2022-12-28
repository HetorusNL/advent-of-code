from pathlib import Path

from solution.grid import Grid


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        grid = Grid(self.lines)
        self.num_rounds = 1
        while grid.do_round():
            self.num_rounds += 1

    def get_result(self) -> str:
        return f"the round number where no elf moves is: {self.num_rounds}"
