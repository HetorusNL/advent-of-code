from pathlib import Path

from solution.beam import Beam


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        results: list[int] = []
        # add top and bottom row simulation
        for col_idx in range(len(self.lines[0])):
            results.append(self.run_simulation(0, col_idx, "u"))
            results.append(self.run_simulation(0, col_idx, "d"))
        # add left and right col simulation
        for row_idx in range(len(self.lines)):
            results.append(self.run_simulation(row_idx, 0, "u"))
            results.append(self.run_simulation(row_idx, 0, "d"))
        self.result = max(results)

    def run_simulation(self, row, col, direction):
        beams: list[Beam] = [Beam(row, col, direction, self.lines)]
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
        result = 0
        for row in grid.values():
            for pos in row.values():
                if pos:
                    result += 1
        return result

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
