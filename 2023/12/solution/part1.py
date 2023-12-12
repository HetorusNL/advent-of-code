from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        for line in self.lines:
            self.parse_line(line)

    def parse_line(self, line: str):
        springs, values_str = line.split(" ")
        values = list(map(int, values_str.split(",")))
        num_unknown = springs.count("?")
        damaged_springs_left = sum(values) - springs.count("#")
        for i in range(2**num_unknown):
            attempt = bin(i)[2:].zfill(num_unknown)
            # must be the correct number of damaged springs
            if attempt.count("1") != damaged_springs_left:
                continue
            parsed_line = self.replace_attempt(springs, attempt)
            if self.spring_correct(values, parsed_line):
                self.result += 1

    def replace_attempt(self, springs: str, attempt) -> str:
        attempt = attempt.replace("1", "#")
        attempt = attempt.replace("0", ".")
        for char in attempt:
            springs = springs.replace("?", char, 1)
        return springs

    def spring_correct(self, values: list[int], parse_line: str):
        spring_groups = list(map(len, filter(lambda a: a, parse_line.split("."))))
        return spring_groups == values

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
