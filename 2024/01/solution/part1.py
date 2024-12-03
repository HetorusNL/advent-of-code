from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        left: list[int] = []
        right: list[int] = []
        for entry in self.lines:
            values = entry.split(" ")
            left.append(int(values[0]))
            right.append(int(values[-1]))
        left = sorted(left)
        right = sorted(right)
        self.result = 0
        for i in range(len(left)):
            self.result += max(left[i], right[i]) - min(left[i], right[i])

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
