from pathlib import Path

from solution.common import Common


class Part2(Common):
    def __init__(self, file: Path):
        Common.__init__(self, file)

    def part_specific_parse(self):
        Common.part_specific_parse(self)
        # unfold the paper
        self.springs = "?".join([self.springs] * 5)
        self.values = self.values * 5

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
