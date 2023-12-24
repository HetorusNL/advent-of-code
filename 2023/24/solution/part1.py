from pathlib import Path

from solution.hailstone import Hailstone


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.min_value = 200000000000000
        self.max_value = 400000000000000

    def solve(self) -> None:
        print("solving...")
        self.hailstones: list[Hailstone] = []
        for line in self.lines:
            self.hailstones.append(Hailstone(line))

        # calculate all intersections
        num_intersections = 0
        calculations = 0
        for first_idx in range(len(self.hailstones)):
            for idx in range(first_idx + 1, len(self.hailstones)):
                calculations += 1
                hailstone1 = self.hailstones[first_idx]
                hailstone2 = self.hailstones[idx]
                num_intersections += hailstone1.intersects_in_bounds(hailstone2, self.min_value, self.max_value)
        self.result = num_intersections

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
