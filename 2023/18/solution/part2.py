from pathlib import Path


class Part2:
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
            hex_code = line.split(" ")[-1][2:-1]
            direction = {0: "R", 1: "D", 2: "L", 3: "U"}[int(hex_code[-1])]
            num_meter = int(hex_code[:-1], 16)
            print(direction, num_meter)
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
        self.result = 0
        trench = 0
        grid_length = len(self.grid)
        chunk = grid_length // 100
        current_percentage = 0
        for row_idx, row in enumerate(self.grid):
            if row_idx // chunk > current_percentage:
                current_percentage = row_idx // chunk
                print(f"processing rows: {current_percentage}%")
            inside = False
            entrance = ""
            last_col = sorted(self.grid[row].keys())[0] - 2
            for col in sorted(self.grid[row].keys()):
                trench += 1
                if col != last_col + 1:
                    if inside:
                        self.result += col - last_col - 1
                if self.grid.get(row - 1, {}).get(col) and self.grid.get(row + 1, {}).get(col):
                    inside = not inside
                elif entrance == "D" and self.grid.get(row - 1, {}).get(col):
                    inside = not inside
                elif entrance == "U" and self.grid.get(row + 1, {}).get(col):
                    inside = not inside
                elif entrance == "U" and self.grid.get(row - 1, {}).get(col):
                    entrance = ""
                elif entrance == "D" and self.grid.get(row + 1, {}).get(col):
                    entrance = ""
                elif self.grid.get(row - 1, {}).get(col):
                    entrance = "U"
                elif self.grid.get(row + 1, {}).get(col):
                    entrance = "D"
                last_col = col
        self.result += trench

    def add_to_grid(self, row: int, col: int):
        if row not in self.grid:
            self.grid[row] = {}
        self.grid[row][col] = True

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
