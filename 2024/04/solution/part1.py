from pathlib import Path


class Part1:
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

    def test_xmas(self, x: int, y: int):
        # test right
        if self.at(x + 1, y, "M") and self.at(x + 2, y, "A") and self.at(x + 3, y, "S"):
            self.result += 1
        # test left
        if self.at(x - 1, y, "M") and self.at(x - 2, y, "A") and self.at(x - 3, y, "S"):
            self.result += 1
        # test up
        if self.at(x, y + 1, "M") and self.at(x, y + 2, "A") and self.at(x, y + 3, "S"):
            self.result += 1
        # test down
        if self.at(x, y - 1, "M") and self.at(x, y - 2, "A") and self.at(x, y - 3, "S"):
            self.result += 1

        # test all diagonals
        # test right-up
        if self.at(x + 1, y + 1, "M") and self.at(x + 2, y + 2, "A") and self.at(x + 3, y + 3, "S"):
            self.result += 1
        # test right-down
        if self.at(x + 1, y - 1, "M") and self.at(x + 2, y - 2, "A") and self.at(x + 3, y - 3, "S"):
            self.result += 1
        # test left-down
        if self.at(x - 1, y - 1, "M") and self.at(x - 2, y - 2, "A") and self.at(x - 3, y - 3, "S"):
            self.result += 1
        # test left-up
        if self.at(x - 1, y + 1, "M") and self.at(x - 2, y + 2, "A") and self.at(x - 3, y + 3, "S"):
            self.result += 1

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.at(x, y, "X"):
                    # found potential start of XMAS in any direction, start test
                    self.test_xmas(x, y)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
