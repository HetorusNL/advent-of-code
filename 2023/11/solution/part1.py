from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        # expand columns
        height = len(self.lines)
        for col_idx in reversed(range(len(self.lines[0]))):
            if all(self.lines[row][col_idx] == "." for row in range(height)):
                for row in range(height):
                    self.lines[row] = self.lines[row][:col_idx] + "." + self.lines[row][col_idx:]

        # expand rows
        width = len(self.lines[0])
        for row_idx in reversed(range(len(self.lines))):
            if self.lines[row_idx].count(".") == width:
                self.lines.insert(row_idx, "." * width)

        # find galaxies
        galaxies: dict[int, list[int]] = {}
        for row_idx, row in enumerate(self.lines):
            for col_idx, col in enumerate(row):
                if col == "#":
                    galaxies[len(galaxies)] = [row_idx, col_idx]

        # iterate galaxies
        shortest_paths: list[int] = []
        for start_galaxy_idx in range(len(galaxies)):
            for end_galaxy_idx in range(start_galaxy_idx + 1, len(galaxies)):
                delta_row = abs(galaxies[start_galaxy_idx][0] - galaxies[end_galaxy_idx][0])
                delta_col = abs(galaxies[start_galaxy_idx][1] - galaxies[end_galaxy_idx][1])
                shortest_paths.append(delta_row + delta_col)
        self.result = sum(shortest_paths)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
