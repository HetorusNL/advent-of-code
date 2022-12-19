from pathlib import Path

from solution.chamber import Chamber


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.line = f.readline().strip()

    def solve(self) -> None:
        print("solving...")
        chamber = Chamber(self.line)
        for _ in range(2022):
            chamber.fall_rock()
        self.tower_height = chamber.tower_height

    def get_result(self) -> str:
        return f"the height of the rock tower after 2022 is: {self.tower_height}"
