from enum import auto
from enum import IntEnum
from pathlib import Path


class Dir(IntEnum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Pos:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.width: int = len(self.lines[0])
        self.height: int = len(self.lines)
        # pos is the position on the grid with the origin at the left bottom
        pos: Pos | None = None
        for row_idx, row in enumerate(self.lines):
            for col_idx, col in enumerate(row):
                if col == "^":
                    pos = Pos(col_idx, self.height - row_idx - 1)
                    self.lines[row_idx] = self.lines[row_idx].replace("^", ".")
        self.lines_copy = self.lines.copy()
        assert pos is not None
        self.pos: Pos = pos
        self.initial_pos = Pos(pos.x, pos.y)
        self.move_grid: dict[int, bool] = {}
        self.dir: Dir = Dir.UP
        self.initial_dir = self.dir

    def is_outside(self, pos: Pos):
        # return whether we're outside of the movable grid
        if pos.x < 0 or pos.x >= self.width:
            return True
        if pos.y < 0 or pos.y >= self.height:
            return True

    def can_move(self, pos: Pos):
        # return whether the position is not blocked,
        # can be outside of the movable grid
        if self.is_outside(pos):
            return True
        return self.lines[self.height - pos.y - 1][pos.x] == "."

    def position_hash(self, pos: Pos) -> int:
        # use an int hash instead, as it is somewhat faster
        return pos.x + pos.y * self.width + int(self.dir) * self.width * self.height

    def add_pos(self, pos: Pos):
        self.move_grid[self.position_hash(pos)] = True

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        for x in range(self.width):
            for y in range(self.height):
                if x == self.initial_pos.x and y == self.initial_pos.y:
                    # skip adding an obstacle on the initial position
                    continue
                pos: Pos = Pos(x, y)
                if self.can_move(pos) and not self.is_outside(pos):
                    # simulate with an obstacle added to this position
                    self.run_simulation(pos)

    def add_obstacle(self, pos: Pos):
        # start with the initial set of lines
        self.lines = self.lines_copy.copy()
        line_idx: int = self.height - pos.y - 1
        line = list(self.lines[line_idx])
        assert line[pos.x] != "#"
        line[pos.x] = "#"
        self.lines[line_idx] = "".join(line)

    def in_cycle(self):
        position_hash = self.position_hash(self.pos)
        return self.move_grid.get(position_hash)

    def run_simulation(self, obstacle_pos: Pos):
        # create a new map with an obstacle at pos
        self.add_obstacle(obstacle_pos)
        # clear the previous map
        self.move_grid.clear()
        # reset the starting position
        self.pos = Pos(self.initial_pos.x, self.initial_pos.y)
        # reset the starting direction
        self.dir = self.initial_dir
        # walk on the grid until we're out of the grid or detect a cycle
        while True:
            # if we're outside of the movable grid, break
            if self.is_outside(self.pos):
                return
            # check whether we're in a cycle
            if self.in_cycle():
                self.result += 1
                return
            # add the current position to the move grid
            self.add_pos(self.pos)
            # move to the next position
            match self.dir:
                case Dir.UP:
                    pos: Pos = Pos(self.pos.x, self.pos.y + 1)
                    if self.can_move(pos):
                        self.pos = pos
                    else:
                        self.dir = Dir.RIGHT
                case Dir.RIGHT:
                    pos: Pos = Pos(self.pos.x + 1, self.pos.y)
                    if self.can_move(pos):
                        self.pos = pos
                    else:
                        self.dir = Dir.DOWN
                case Dir.DOWN:
                    pos: Pos = Pos(self.pos.x, self.pos.y - 1)
                    if self.can_move(pos):
                        self.pos = pos
                    else:
                        self.dir = Dir.LEFT
                case Dir.LEFT:
                    pos: Pos = Pos(self.pos.x - 1, self.pos.y)
                    if self.can_move(pos):
                        self.pos = pos
                    else:
                        self.dir = Dir.UP

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
