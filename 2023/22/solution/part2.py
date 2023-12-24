from pathlib import Path

from solution.brick import Brick


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.bricks: list[Brick] = []
        self.space: dict[int, dict[int, dict[int, Brick]]] = {}
        self.fallen_space: dict[int, dict[int, dict[int, Brick]]] = {}
        for line in self.lines:
            self.bricks.append(Brick(line, self.bricks, self.space, self.fallen_space))
        for brick in self.bricks:
            brick.fall()
        bricks_that_fall_on_disintegration = [brick.bricks_that_fall_on_disintegration() for brick in self.bricks]
        for brick in self.bricks:
            assert brick.has_fallen
        self.result = sum(bricks_that_fall_on_disintegration)

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
