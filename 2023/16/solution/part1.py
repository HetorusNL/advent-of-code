from pathlib import Path

from solution.beam import Beam


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        beams: list[Beam] = [Beam(0, 0, "r", self.lines)]
        grid: dict[int, dict[int, list[str]]] = {}
        for row_idx in range(len(self.lines)):
            grid[row_idx] = {}
            for col_idx in range(len(self.lines[0])):
                grid[row_idx][col_idx] = []

        while beams:
            new_beams: list[Beam] = []
            for beam in beams:
                # add energy to the grid
                if beam.direction in grid[beam.row][beam.col]:
                    continue
                grid[beam.row][beam.col].append(beam.direction)
                # get next beam(s)
                new_beams.extend(beam.get_next())
            beams = new_beams
        self.result = 0
        for row in grid.values():
            for pos in row.values():
                if pos:
                    self.result += 1

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
