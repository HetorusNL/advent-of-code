from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.height: int = len(self.lines)
        self.width: int = len(self.lines[0])

    def pos(self, x: int, y: int):
        # test that y is within the grid, otherwise return "."
        if y >= self.height or y < 0:
            return "."
        # test that x is within the grid, otherwise return "."
        if x >= self.width or x < 0:
            return "."
        # otherwise return the character in the grid, origin left bottom
        return self.lines[self.height - y - 1][x]

    def at(self, x: int, y: int, char: str):
        # returns that the char at (x, y) is equal to char ("." is special)
        return self.pos(x, y) == char

    def test_cross(self, x: int, y: int):
        # start at the top right of the initial x-mas pos grid
        x += 2
        # search for SAM to the bottom left
        if self.at(x, y, "S") and self.at(x - 1, y - 1, "A") and self.at(x - 2, y - 2, "M"):
            self.result += 1
        # search for MAS to the bottom left
        if self.at(x, y, "M") and self.at(x - 1, y - 1, "A") and self.at(x - 2, y - 2, "S"):
            self.result += 1

    def test_xmas(self, x: int, y: int):
        if self.at(x, y, "S"):
            # search for SAM to the bottom right
            if self.at(x + 1, y - 1, "A") and self.at(x + 2, y - 2, "M"):
                # found! now check if we can make the X-MAS cross
                self.test_cross(x, y)
        elif self.at(x, y, "M"):
            # search for MAS to the bottom right
            if self.at(x + 1, y - 1, "A") and self.at(x + 2, y - 2, "S"):
                # found! now check if we can make the X-MAS cross
                self.test_cross(x, y)

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.at(x, y, "S") or self.at(x, y, "M"):
                    # found potential start of X-MAS to bottom-right, start test
                    self.test_xmas(x, y)

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
