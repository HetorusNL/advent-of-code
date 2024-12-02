from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        for line in self.lines:
            previous, *values = map(int, line.split())
            fail = False
            if values[0] > previous:
                # all must be increasing
                for value in values:
                    if value - previous in [1, 2, 3]:
                        previous = value
                    else:
                        fail = True
                if not fail:
                    self.result += 1
            elif values[0] < previous:
                # all must be decreasing
                for value in values:
                    if previous - value in [1, 2, 3]:
                        previous = value
                    else:
                        fail = True
                if not fail:
                    self.result += 1

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
