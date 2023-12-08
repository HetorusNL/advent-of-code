from pathlib import Path
import re
import math


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.instructions = [0 if char == "L" else 1 for char in self.lines[0]]
        self._map: dict[str, list[str]] = {}
        for line in self.lines[2:]:
            match = re.match(r"(?P<location>[A-Z0-9]*) = \((?P<left>[A-Z0-9]*), (?P<right>[A-Z0-9]*)\)", line)
            assert match
            self._map[match["location"]] = [match["left"], match["right"]]
        self.result = math.lcm(*self.run_map())

    def run_map(self):
        steps = 0
        locations = list(filter(lambda location: location.endswith("A"), self._map.keys()))
        cycle_length = [0] * len(locations)
        while True:
            for instruction in self.instructions:
                steps += 1
                for location_idx in range(len(locations)):
                    locations[location_idx] = self._map[locations[location_idx]][instruction]
                    if locations[location_idx].endswith("Z") and cycle_length[location_idx] == 0:
                        cycle_length[location_idx] = steps
                if 0 not in cycle_length:
                    return cycle_length

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
