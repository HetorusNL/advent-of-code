from pathlib import Path
import re


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.instructions = [0 if char == "L" else 1 for char in self.lines[0]]
        self._map = {}
        for line in self.lines[2:]:
            match = re.match(r"(?P<location>[A-Z]*) = \((?P<left>[A-Z]*), (?P<right>[A-Z]*)\)", line)
            assert match
            self._map[match["location"]] = [match["left"], match["right"]]
        self.result = self.run_map()

    def run_map(self):
        steps = 0
        location = "AAA"
        while True:
            for instruction in self.instructions:
                location = self._map[location][instruction]
                steps += 1
            if location == "ZZZ":
                return steps

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
