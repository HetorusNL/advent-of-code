from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.time = int("".join(line for line in self.lines[0].split(" ")[1:] if line))
        self.distance = int("".join(line for line in self.lines[1].split(" ")[1:] if line))

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        for charge_time in range(self.time):
            distance = (self.time - charge_time) * charge_time
            if distance > self.distance:
                self.result += 1

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
