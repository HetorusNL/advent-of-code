from pathlib import Path

from solution.robot_factory import RobotFactory


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        robot_factory = RobotFactory(self.lines)
        self.quality_level = robot_factory.run_for_minutes_part_1(24)

    def get_result(self) -> str:
        return f"the quality level of all the blueprints is: {self.quality_level}"
