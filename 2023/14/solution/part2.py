from pathlib import Path


class Part2:
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
        cycle_counter = 0
        cache = {}
        for cycle_counter in range(1, 1000000000 + 1):
            self.run_cycle()
            state = self.get_state()
            print(f"weight: {self.get_weight()}")
            if state in cache:
                print(f"found cycle at {cycle_counter} to cycle {cache[state]}")
                single_cycle = cycle_counter - cache[state]
                print(single_cycle)
                cycles_left = 1000000000 - cache[state] - single_cycle
                cycles_from_cycle_start = cycles_left % single_cycle
                print(f"cycles_from_cycle_start {cycles_from_cycle_start}")
                # simply run the remaining cycles
                for _ in range(cycles_from_cycle_start):
                    self.run_cycle()
                break
            cache[state] = cycle_counter
        self.result = self.get_weight()

    def get_state(self):
        return "".join(["".join(row) for row in self.grid])

    def run_cycle(self):
        self.move_north()
        self.move_west()
        self.move_south()
        self.move_east()

    def move_north(self):
        for row_idx in range(1, self.height):
            for col_idx in range(self.width):
                if self.grid[row_idx][col_idx] == "O" and self.grid[row_idx - 1][col_idx] == ".":
                    for new_row_idx in range(row_idx - 1, -1, -1):
                        if self.grid[new_row_idx][col_idx] != ".":
                            # we can move, move the rock up
                            self.grid[new_row_idx + 1][col_idx] = "O"
                            self.grid[row_idx][col_idx] = "."
                            break
                        if new_row_idx == 0:
                            # we can move, move the rock up
                            self.grid[new_row_idx][col_idx] = "O"
                            self.grid[row_idx][col_idx] = "."

    def move_west(self):
        for col_idx in range(1, self.width):
            for row_idx in range(self.height):
                if self.grid[row_idx][col_idx] == "O" and self.grid[row_idx][col_idx - 1] == ".":
                    for new_col_idx in range(col_idx - 1, -1, -1):
                        if self.grid[row_idx][new_col_idx] != ".":
                            # we can move, move the rock left
                            self.grid[row_idx][new_col_idx + 1] = "O"
                            self.grid[row_idx][col_idx] = "."
                            break
                        if new_col_idx == 0:
                            # we can move, move the rock left
                            self.grid[row_idx][new_col_idx] = "O"
                            self.grid[row_idx][col_idx] = "."

    def move_south(self):
        for row_idx in range(self.height - 1, 0, -1):
            for col_idx in range(self.width):
                if self.grid[row_idx][col_idx] == "." and self.grid[row_idx - 1][col_idx] == "O":
                    for new_row_idx in range(row_idx, self.height):
                        if self.grid[new_row_idx][col_idx] != ".":
                            # we can move, move the rock down
                            self.grid[new_row_idx - 1][col_idx] = "O"
                            self.grid[row_idx - 1][col_idx] = "."
                            break
                        if new_row_idx == self.height - 1:
                            # we can move, move the rock down
                            self.grid[new_row_idx][col_idx] = "O"
                            self.grid[row_idx - 1][col_idx] = "."

    def move_east(self):
        # move rocks west
        for col_idx in range(self.width - 1, 0, -1):
            for row_idx in range(self.height):
                if self.grid[row_idx][col_idx] == "." and self.grid[row_idx][col_idx - 1] == "O":
                    for new_col_idx in range(col_idx, self.width):
                        if self.grid[row_idx][new_col_idx] != ".":
                            # we can move, move the rock right
                            self.grid[row_idx][new_col_idx - 1] = "O"
                            self.grid[row_idx][col_idx - 1] = "."
                            break
                        if new_col_idx == self.width - 1:
                            # we can move, move the rock right
                            self.grid[row_idx][new_col_idx] = "O"
                            self.grid[row_idx][col_idx - 1] = "."

    def get_weight(self):
        weight = 0
        for row_idx in range(self.height):
            weight += "".join(self.grid[row_idx]).count("O") * (self.height - row_idx)
        return weight

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
