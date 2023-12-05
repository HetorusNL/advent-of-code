from pathlib import Path
import re

from solution.map_value import MapValue
from solution.seed_range import SeedRange


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

        seeds = [int(seed.strip()) for seed in self.lines[0].split(":")[1].split(" ") if seed]
        self.seed_ranges: list[SeedRange] = []
        for i in range(len(seeds) // 2):
            self.seed_ranges.append(SeedRange(seeds[i * 2], seeds[i * 2 + 1]))
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
        _from = None
        _to = "seed"
        seed_ranges = self.seed_ranges
        while _to != "location":
            _from = _to
            _to = self.word_maps[_from]
            new_seed_ranges: list[SeedRange] = []
            for seed_range in seed_ranges:
                while not seed_range.is_done():
                    value = seed_range.value
                    found = False
                    for value_map in self.value_maps[_from]:
                        if value_map.is_in(value):
                            new_value = value_map.get_mapped_value(value)
                            seed_range_left = seed_range.values_left()
                            value_map_left = value_map.values_left(value)
                            new_seed_ranges.append(SeedRange(new_value, min(seed_range_left, value_map_left)))
                            seed_range.value = value_map.src + value_map.length
                            found = True
                            break
                    if not found:
                        start_values = [value_map.src for value_map in self.value_maps[_from]]
                        start_values = list(filter(lambda start_value: start_value > value, start_values))
                        if start_values:
                            start_value = min(start_values)
                            seed_range_left = seed_range.values_left()
                            to_start_value_range_left = start_value - value
                            new_seed_ranges.append(SeedRange(value, min(seed_range_left, to_start_value_range_left)))
                            seed_range.value = start_value
                        else:
                            new_seed_ranges.append(SeedRange(value, seed_range.values_left()))
                            seed_range.value += seed_range.values_left()
            seed_ranges = new_seed_ranges

        self.result = min(seed_range.start for seed_range in seed_ranges)

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
