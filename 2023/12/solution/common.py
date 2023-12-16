from pathlib import Path

from solution.spring import Spring


class Common:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        for line in self.lines:
            self.parse_line(line)

    def part_specific_parse(self):
        pass

    def parse_line(self, line: str):
        self.springs, values_str = line.split(" ")
        self.values: list[int] = list(map(int, values_str.split(",")))

        self.part_specific_parse()

        self.num_values = len(self.values)
        length = len(self.springs)
        self.cache: dict[int, dict[str, Spring]] = {}
        for i in range(length):
            self.cache[i] = {}
        self.cache[0][""] = Spring(self.springs, 0)

        for springs_idx in range(length):
            for spring in self.cache[springs_idx].values():
                if spring.springs[springs_idx] == "?":
                    # try adding a '.'
                    self.add_operational(spring, springs_idx)
                    # try adding a '#' (thus a value)
                    self.add_damaged(spring, springs_idx)
                elif spring.springs[springs_idx] == "#":
                    # try adding a value
                    self.add_damaged(spring, springs_idx)
                elif spring.springs[springs_idx] == ".":
                    self.add_operational(spring, springs_idx)
                else:
                    assert False

    def add_operational(self, spring: Spring, springs_idx: int):
        new_springs = spring.springs[:springs_idx] + "." + spring.springs[springs_idx + 1 :]
        new_spring = Spring(new_springs, spring.value_idx)
        new_spring.number_of_arrangements = spring.number_of_arrangements
        self.add_if_solvable(new_spring, springs_idx + 1)

    def add_damaged(self, spring: Spring, springs_idx: int):
        # test if the next value can be added
        value = self.values[spring.value_idx]
        if "." in spring.springs[springs_idx : springs_idx + value]:
            return
        # is this the last value?
        if spring.value_idx + 1 < self.num_values:
            # not the last value
            if spring.springs[springs_idx + value] == "#":
                return
            new_springs = spring.springs[:springs_idx] + "#" * value + "." + spring.springs[springs_idx + value + 1 :]
            new_spring = Spring(new_springs, spring.value_idx + 1)
            new_spring.number_of_arrangements = spring.number_of_arrangements
            self.add_if_solvable(new_spring, springs_idx + value + 1)
        else:
            # this is the last value
            new_springs: str = spring.springs[:springs_idx] + "#" * value + spring.springs[springs_idx + value :]
            new_spring = Spring(new_springs, spring.value_idx + 1)
            new_spring.number_of_arrangements = spring.number_of_arrangements
            self.add_if_solvable(new_spring, springs_idx + value)

    def add_if_solvable(self, spring: Spring, springs_idx: int):
        if self.is_solvable(spring, springs_idx):
            if self.is_finished(spring, springs_idx):
                self.result += spring.number_of_arrangements
            else:
                spring_hash = f"{springs_idx},{spring.value_idx}"
                if spring_hash in self.cache[springs_idx]:
                    self.cache[springs_idx][spring_hash].number_of_arrangements += spring.number_of_arrangements
                else:
                    self.cache[springs_idx][spring_hash] = spring

    def is_solvable(self, spring: Spring, springs_idx: int):
        values_left = self.values[spring.value_idx :]
        sum_values_left = sum(values_left)
        space_needed = sum_values_left + len(values_left) - 1
        springs_chars_left = spring.springs[springs_idx:]
        if space_needed > len(springs_chars_left):
            return False
        if not values_left:
            if springs_chars_left.count("#") > 0:
                return False
        return True

    def is_finished(self, spring: Spring, springs_idx: int):
        if spring.value_idx < self.num_values:
            return False
        if "#" in spring.springs[springs_idx:]:
            return False
        return True
