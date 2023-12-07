from pathlib import Path

from solution.hand1 import Hand1


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        hands: list[Hand1] = []
        for line in self.lines:
            cards, bid = line.split(" ")
            hands.append(Hand1(cards, bid))
        hands = sorted(hands)
        self.result = 0
        for hand_idx, hand in enumerate(hands):
            self.result += hand.bid * (hand_idx + 1)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
