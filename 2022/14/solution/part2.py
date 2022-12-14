from pathlib import Path

from solution.grid import Grid


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        grid = Grid(self.lines)
        grid.do_sand_part_2()
        self.num_sand_units = grid.get_num_sand_units()

    def get_result(self) -> str:
        return f"the number of fallen sand units of part 2 is: {self.num_sand_units}"
