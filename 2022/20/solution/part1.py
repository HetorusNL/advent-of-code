from pathlib import Path

from solution.sequence import Sequence


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        sequence = Sequence(self.lines)
        sequence.mixing()
        self.grove_coordinates = sequence.get_grove_coordinates()

    def get_result(self) -> str:
        return f"the grove coordinates are: {self.grove_coordinates}"
