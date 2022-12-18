from pathlib import Path

from solution.volcano import Volcano


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        volcano = Volcano(self.lines)
        self.pressure_released = 0
        # self.pressure_released = volcano.run_for_minutes(30)

    def get_result(self) -> str:
        return f"the maximum amount of pressure released is: {self.pressure_released}"
