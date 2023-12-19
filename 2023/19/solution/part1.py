from pathlib import Path
import re

from solution.part import Part
from solution.workflow import Workflow


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.worksflows: dict[str, Workflow] = {}
        self.parts: list[Part] = []
        for line in self.lines:
            if match := re.match(r"^(?P<name>[a-z]+){(?P<rules>.*)}$", line):
                self.worksflows[match["name"]] = Workflow(match["rules"])
            elif match := re.match(r"^{(?P<values>.*)}$", line):
                self.parts.append(Part(match["values"]))
            else:
                assert not line

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        for part in self.parts:
            workflow = "in"
            while True:
                workflow = self.worksflows[workflow].process(part)
                if workflow == "A":
                    self.result += part.value
                    break
                if workflow == "R":
                    break

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
