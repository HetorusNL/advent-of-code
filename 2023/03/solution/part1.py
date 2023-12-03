from pathlib import Path

from solution.grid import Grid


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        grid = Grid(self.lines)
        numbers = grid.numbers_adjecent_to_symbols()
        self.result = sum(numbers)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
