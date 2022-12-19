from pathlib import Path

from solution.grid import Grid


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.exposed_sides = Grid(self.lines).get_exposed_exterior_sides()

    def get_result(self) -> str:
        return f"the number of exposed exterior sides of the lava druplet is: {self.exposed_sides}"
