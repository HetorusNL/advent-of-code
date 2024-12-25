from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.result: str = "woo, we've finished AoC 2024! 🥳"

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
