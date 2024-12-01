from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        left = []
        right = []
        for entry in self.lines:
            values = entry.split(" ")
            left.append(int(values[0]))
            right.append(int(values[-1]))
        left = sorted(left)
        right = sorted(right)
        self.result = 0
        for entry in left:
            self.result += entry * right.count(entry)

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
