from pathlib import Path

from solution.keep_away import KeepAway


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        keep_away = KeepAway(self.lines)
        keep_away.simulate_rounds(10000, divide_worry_level=False)
        self.monkey_business = keep_away.monkey_business

    def get_result(self) -> str:
        return f"the monkey business level after 10000 rounds is: {self.monkey_business}"
