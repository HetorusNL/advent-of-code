from pathlib import Path

from solution.sequence import Sequence


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        sequence = Sequence(self.lines)
        sequence.decrypted_mixing()
        self.decrypted_grove_coordinates = sequence.get_grove_coordinates()

    def get_result(self) -> str:
        return f"the decrypted grove coordinates are: {self.decrypted_grove_coordinates}"
