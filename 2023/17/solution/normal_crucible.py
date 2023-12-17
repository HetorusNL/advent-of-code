class Crucible:
    def __init__(self, grid: dict[int, dict[int, int]], row: int, col: int, dir: str, dir_cnt: int, heat_loss: int):
        self.grid = grid
        self.row = row
        self.col = col
        self.dir = dir
        self.dir_cnt = dir_cnt
        self.heat_loss = heat_loss

    def hash(self):
        return f"{self.row},{self.col},{self.dir},{self.dir_cnt}"

    def get_next_pos(self) -> list["Crucible"]:
        pos: list["Crucible"] = []
        match self.dir:
            case "u":
                if self.dir_cnt < 3:
                    if self.row > 0:
                        heat_loss = self.heat_loss + self.grid[self.row - 1][self.col]
                        pos.append(Crucible(self.grid, self.row - 1, self.col, self.dir, self.dir_cnt + 1, heat_loss))
                if self.col > 0:
                    heat_loss = self.heat_loss + self.grid[self.row][self.col - 1]
                    pos.append(Crucible(self.grid, self.row, self.col - 1, "l", 1, heat_loss))
                if self.col < len(self.grid[0]) - 1:
                    heat_loss = self.heat_loss + self.grid[self.row][self.col + 1]
                    pos.append(Crucible(self.grid, self.row, self.col + 1, "r", 1, heat_loss))
            case "d":
                if self.dir_cnt < 3:
                    if self.row < len(self.grid) - 1:
                        heat_loss = self.heat_loss + self.grid[self.row + 1][self.col]
                        pos.append(Crucible(self.grid, self.row + 1, self.col, self.dir, self.dir_cnt + 1, heat_loss))
                if self.col > 0:
                    heat_loss = self.heat_loss + self.grid[self.row][self.col - 1]
                    pos.append(Crucible(self.grid, self.row, self.col - 1, "l", 1, heat_loss))
                if self.col < len(self.grid[0]) - 1:
                    heat_loss = self.heat_loss + self.grid[self.row][self.col + 1]
                    pos.append(Crucible(self.grid, self.row, self.col + 1, "r", 1, heat_loss))
            case "l":
                if self.dir_cnt < 3:
                    if self.col > 0:
                        heat_loss = self.heat_loss + self.grid[self.row][self.col - 1]
                        pos.append(Crucible(self.grid, self.row, self.col - 1, self.dir, self.dir_cnt + 1, heat_loss))
                if self.row > 0:
                    heat_loss = self.heat_loss + self.grid[self.row - 1][self.col]
                    pos.append(Crucible(self.grid, self.row - 1, self.col, "u", 1, heat_loss))
                if self.row < len(self.grid[0]) - 1:
                    heat_loss = self.heat_loss + self.grid[self.row + 1][self.col]
                    pos.append(Crucible(self.grid, self.row + 1, self.col, "d", 1, heat_loss))
            case "r":
                if self.dir_cnt < 3:
                    if self.col < len(self.grid[0]) - 1:
                        heat_loss = self.heat_loss + self.grid[self.row][self.col + 1]
                        pos.append(Crucible(self.grid, self.row, self.col + 1, self.dir, self.dir_cnt + 1, heat_loss))
                if self.row > 0:
                    heat_loss = self.heat_loss + self.grid[self.row - 1][self.col]
                    pos.append(Crucible(self.grid, self.row - 1, self.col, "u", 1, heat_loss))
                if self.row < len(self.grid[0]) - 1:
                    heat_loss = self.heat_loss + self.grid[self.row + 1][self.col]
                    pos.append(Crucible(self.grid, self.row + 1, self.col, "d", 1, heat_loss))
        return pos
