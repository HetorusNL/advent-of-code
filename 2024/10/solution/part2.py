from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.width: int = len(self.lines[0])
        self.height: int = len(self.lines)

    def is_outside(self, x: int, y: int):
        # return whether we're outside of the grid
        if x < 0 or x >= self.width:
            return True
        if y < 0 or y >= self.height:
            return True

    def get_pos(self, x: int, y: int) -> int | None:
        # return None when outside of the grid, otherwise the int value at the location
        if self.is_outside(x, y):
            return None
        return int(self.lines[self.height - y - 1][x])

    def next_pos(self, x: int, y: int):
        # return all positions left, right, up, down from the current pos
        next_pos: list[tuple[int, int]] = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        return next_pos

    def step_path(self, x: int, y: int, current_value: int):
        # check which of the next pos has the correct value
        next_value = current_value + 1
        for next_x, next_y in self.next_pos(x, y):
            if self.get_pos(next_x, next_y) == next_value:
                if next_value == 9:
                    # if we're at 9, we found a trail, increment result
                    self.result += 1
                else:
                    # otherwise recurse onward till the 9
                    self.step_path(next_x, next_y, next_value)

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        # loop through all positions, starting the recurse at every 0
        for x in range(self.width):
            for y in range(self.height):
                if self.get_pos(x, y) == 0:
                    # recurse into the position
                    self.step_path(x, y, 0)

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
