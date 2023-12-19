from pathlib import Path
import re

from solution.part import Part
from solution.part_range import PartRange
from solution.workflow import Workflow
from solution.workflow_path import WorkflowPath


class Part2:
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
        paths: list[WorkflowPath] = [WorkflowPath("in", PartRange())]
        finished_ranges: list[PartRange] = []
        while paths:
            new_paths: list[WorkflowPath] = []
            for path in paths:
                part_range = path.part_range
                for rule in self.worksflows[path.next_workflow].rules:
                    pass_range, pass_workflow, fail_range = rule.get_part_ranges(part_range)
                    if pass_range.solvable():
                        if pass_workflow == "A":
                            finished_ranges.append(pass_range)
                        elif pass_workflow != "R":
                            new_paths.append(WorkflowPath(pass_workflow, pass_range))
                    if fail_range:
                        part_range = fail_range
            paths = new_paths
        self.result = sum([range.result for range in finished_ranges])

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
