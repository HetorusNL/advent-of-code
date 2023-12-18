from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        # initialize the grid
        row = 0
        col = 0
        self.grid: dict[int, dict[int, bool]] = {}
        self.grid[row] = {col: True}
        # create the trench
        for line in self.lines:
            direction, num_meter, color = line.split(" ")
            for _ in range(int(num_meter)):
                match direction:
                    case "U":
                        row -= 1
                    case "D":
                        row += 1
                    case "L":
                        col -= 1
                    case "R":
                        col += 1
                self.add_to_grid(row, col)

        # do flood fill
        lowest_row = min(self.grid.keys())
        lowest_row_values = self.grid[lowest_row].keys()
        center_col = abs(min(lowest_row_values) - max(lowest_row_values)) // 2
        # find interior
        row = lowest_row
        col = center_col
        found_border = False
        while row in self.grid:
            if found_border:
                if not self.grid[row].get(col):
                    break  # found the interior
            else:
                if self.grid[row].get(col):
                    found_border = True
            row += 1
        # start flood fill
        flood_pos = [[row, col]]
        while flood_pos:
            new_flood_pos = []
            for row, col in flood_pos:
                if not self.grid[row - 1].get(col):
                    self.grid[row - 1][col] = True
                    new_flood_pos.append([row - 1, col])
                if not self.grid[row + 1].get(col):
                    self.grid[row + 1][col] = True
                    new_flood_pos.append([row + 1, col])
                if not self.grid[row].get(col - 1):
                    self.grid[row][col - 1] = True
                    new_flood_pos.append([row, col - 1])
                if not self.grid[row].get(col + 1):
                    self.grid[row][col + 1] = True
                    new_flood_pos.append([row, col + 1])
            flood_pos = new_flood_pos

        self.result = 0
        for row in self.grid:
            for col in self.grid[row]:
                self.result += 1

    def add_to_grid(self, row: int, col: int):
        if row not in self.grid:
            self.grid[row] = {}
        self.grid[row][col] = True

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
