from pathlib import Path

from solution.hand2 import Hand2


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        hands: list[Hand2] = []
        for line in self.lines:
            cards, bid = line.split(" ")
            hands.append(Hand2(cards, bid))
        hands = sorted(hands)
        self.result = 0
        for hand_idx, hand in enumerate(hands):
            self.result += hand.bid * (hand_idx + 1)

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
