from pathlib import Path

from solution.common import Common


class Part2(Common):
    def __init__(self, file: Path):
        Common.__init__(self, file)
        self.lines = [list(reversed(line)) for line in self.lines]

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
