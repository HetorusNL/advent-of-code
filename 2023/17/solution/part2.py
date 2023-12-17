from pathlib import Path

from solution.ultra_crucible import Crucible


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.grid: dict[int, dict[int, int]] = {}
        for line_idx, line in enumerate(self.lines):
            self.grid[line_idx] = {}
            for col_idx, col in enumerate(line):
                self.grid[line_idx][col_idx] = int(col)

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        # initial grid_pos setup
        self.grid_pos: dict[int, dict[int, dict[int, dict[str, Crucible]]]] = {}
        self.min_heat_loss: dict[int, dict[int, int]] = {}
        for line_idx, line in enumerate(self.lines):
            self.grid_pos[line_idx] = {}
            self.min_heat_loss[line_idx] = {}
            for col_idx, _ in enumerate(line):
                self.grid_pos[line_idx][col_idx] = {}
                self.min_heat_loss[line_idx][col_idx] = 0
        initial_pos_r = Crucible(self.grid, 0, 1, "r", 1, self.grid[0][1])
        self.grid_pos[0][1] = {self.grid[0][1]: {initial_pos_r.hash(): initial_pos_r}}
        initial_pos_d = Crucible(self.grid, 1, 0, "d", 1, self.grid[1][0])
        self.grid_pos[1][0] = {self.grid[1][0]: {initial_pos_d.hash(): initial_pos_d}}

        # loop until we get to the exit
        heat_loss_value = 0
        self.exit_found = False
        while True:
            print(heat_loss_value)
            for row_idx, row in self.grid_pos.items():
                for col_idx, col in row.items():
                    if heat_loss_value in col:
                        for pos in col[heat_loss_value].values():
                            # get all new Crucible instances and add to the grid_pos if applicable
                            self.process_pos(pos)
                        del col[heat_loss_value]
            heat_loss_value += 1
            if self.exit_found and heat_loss_value >= self.result:
                break

    def process_pos(self, pos: Crucible):
        MAX_HEAT_LOSS_DIFF = 50
        for next_pos in pos.get_next_pos():
            # check if finished
            if next_pos.row == (len(self.grid_pos) - 1) and next_pos.col == (len(self.grid_pos[0]) - 1):
                if self.exit_found:
                    self.result = min(self.result, next_pos.heat_loss)
                else:
                    self.result = next_pos.heat_loss
                    self.exit_found = True
                continue
            # otherwise process the next_pos
            if not next_pos.heat_loss in self.grid_pos[next_pos.row][next_pos.col]:
                self.grid_pos[next_pos.row][next_pos.col][next_pos.heat_loss] = {next_pos.hash(): next_pos}
            else:
                current_pos = self.grid_pos[next_pos.row][next_pos.col]
                min_heat_loss = self.min_heat_loss[next_pos.row][next_pos.col]
                if next_pos.heat_loss < (min_heat_loss + MAX_HEAT_LOSS_DIFF):
                    current_pos[next_pos.heat_loss][next_pos.hash()] = next_pos
            if self.min_heat_loss[next_pos.row][next_pos.col] == 0:
                self.min_heat_loss[next_pos.row][next_pos.col] = next_pos.heat_loss
            else:
                self.min_heat_loss[next_pos.row][next_pos.col] = min(
                    self.min_heat_loss[next_pos.row][next_pos.col], next_pos.heat_loss
                )

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
