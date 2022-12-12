from pathlib import Path

from solution.grid import Grid


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        grid = Grid(self.lines)
        self.num_steps_till_end = grid.num_steps_till_end_and_find_start_pos()

    def get_result(self) -> str:
        return f"the number of steps from start till end with optimal start pos: {self.num_steps_till_end}"
