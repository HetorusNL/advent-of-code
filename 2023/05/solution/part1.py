from pathlib import Path
import re

from solution.map_value import MapValue


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

        self.seeds = [int(seed.strip()) for seed in self.lines[0].split(":")[1].split(" ") if seed]
        print(self.seeds)
        self.word_maps: dict[str, str] = {}
        self.value_maps: dict[str, list[MapValue]] = {}
        _from = ""
        _to = ""
        for line in self.lines[2:]:
            if match := re.match(r"(?P<from>[a-z]*)-to-(?P<to>[a-z]*) map:", line):
                _from = match["from"]
                _to = match["to"]
                self.word_maps[_from] = _to
                self.value_maps[_from] = []
            elif line:
                dst, src, length = [int(value.strip()) for value in line.split(" ")]
                self.value_maps[_from].append(MapValue(dst, src, length))

    def solve(self) -> None:
        print("solving...")
        locations = []
        for seed in self.seeds:
            _from = None
            _to = "seed"
            value = seed
            while _to != "location":
                _from = _to
                _to = self.word_maps[_from]
                for value_map in self.value_maps[_from]:
                    if value_map.is_in(value):
                        new_value = value_map.get_mapped_value(value)
                        value = new_value
                        break
            locations.append(value)
        self.result = min(locations)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
