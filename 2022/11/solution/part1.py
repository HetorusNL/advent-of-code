from pathlib import Path

from solution.keep_away import KeepAway


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        keep_away = KeepAway(self.lines)
        keep_away.simulate_rounds(20, divide_worry_level=True)
        self.monkey_business = keep_away.monkey_business

    def get_result(self) -> str:
        return f"the monkey business level after 20 rounds is: {self.monkey_business}"
