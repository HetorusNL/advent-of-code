from pathlib import Path

from solution.robot_factory import RobotFactory


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

        self.lines = [
            "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.",
            "Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.",
        ]

    def solve(self) -> None:
        print("solving...")
        robot_factory = RobotFactory(self.lines)
        self.quality_level = robot_factory.run_for_minutes(24)

    def get_result(self) -> str:
        return f"the quality level of all the blueprints is: {self.quality_level}"
