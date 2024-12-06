from enum import auto
from enum import Enum
from pathlib import Path


class Dir(Enum):
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


class Part1:
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
        assert pos is not None
        self.pos: Pos = pos
        self.move_grid: dict[str, bool] = {}
        self.add_pos(self.pos)
        self.dir: Dir = Dir.UP

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

    def add_pos(self, pos: Pos):
        self.move_grid[str(pos)] = True

    def solve(self) -> None:
        print("solving...")
        # walk on the grid until we're out of the grid or detect a cycle
        while True:
            # if we're outside of the movable grid, break
            if self.is_outside(self.pos):
                break
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

        # as we only store positions that we can move to, the length is the result
        self.result = len(self.move_grid)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
