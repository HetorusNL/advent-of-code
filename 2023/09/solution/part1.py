from pathlib import Path

from solution.common import Common


class Part1(Common):
    def __init__(self, file: Path):
        Common.__init__(self, file)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
