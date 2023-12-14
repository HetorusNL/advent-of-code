from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.grid: list[list[str]] = []
        self.height = len(self.lines)
        self.width = len(self.lines[0])
        for line in self.lines:
            self.grid.append([char for char in line])

    def solve(self) -> None:
        print("solving...")
        while self.run_iteration():
            pass
        self.result = self.get_weight()

    def run_iteration(self):
        rock_moved = False
        for row_idx in range(1, self.height):
            for col_idx in range(self.width):
                if self.grid[row_idx][col_idx] == "O" and self.grid[row_idx - 1][col_idx] == ".":
                    # we can move, move the rock up
                    self.grid[row_idx - 1][col_idx] = "O"
                    self.grid[row_idx][col_idx] = "."
                    rock_moved = True
        return rock_moved

    def get_weight(self):
        weight = 0
        for row_idx in range(self.height):
            weight += "".join(self.grid[row_idx]).count("O") * (self.height - row_idx)
        return weight

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
