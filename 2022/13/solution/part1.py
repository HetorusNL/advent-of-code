from pathlib import Path

from solution.distress_signal import DistressSignal


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.indices_in_right_order = 0
        index = 0
        while self.lines:
            index += 1
            # read left, right and skip the empty line
            left, *self.lines = self.lines
            right, *self.lines = self.lines
            self.lines = self.lines[1:]
            # if it's in the right order, count the index
            if DistressSignal(left, right).is_in_right_order():
                self.indices_in_right_order += index

    def get_result(self) -> str:
        return f"the sum of the indices in the right order are: {self.indices_in_right_order}"
