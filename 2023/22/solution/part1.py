from pathlib import Path

from solution.brick import Brick


class Part1:
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
        can_disintegrate = [brick.can_disintegrate() for brick in self.bricks]
        for brick in self.bricks:
            assert brick.has_fallen
        self.result = sum(can_disintegrate)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
