from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        initialization_sequence = [step.strip() for step in self.lines[0].split(",")]
        for step in initialization_sequence:
            current_value = 0
            for c in step:
                current_value += ord(c)
                current_value *= 17
                current_value %= 256
            self.result += current_value

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
