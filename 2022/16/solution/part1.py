from pathlib import Path

from solution.volcano import Volcano


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        volcano = Volcano(self.lines)
        minutes = 30
        volcano.run_for_minutes(minutes)
        self.pressure_released = volcano.max_pressure_released_for_minute(minutes)

    def get_result(self) -> str:
        return f"the maximum amount of pressure released is: {self.pressure_released}"
