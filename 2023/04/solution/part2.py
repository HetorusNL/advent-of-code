from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        cards = {i: 1 for i in range(len(self.lines))}
        for card_idx, line in enumerate(self.lines):
            line = line.split(":")[1].strip()
            winning, your = line.split("|")
            winning = [winning for winning in winning.split(" ") if winning]
            your = [your for your in your.split(" ") if your]

            good_numbers = 0
            for number in your:
                if number in winning:
                    good_numbers += 1
            for i in range(card_idx + 1, card_idx + 1 + good_numbers):
                cards[i] += cards[card_idx]
        self.scratch_cards = sum(cards.values())

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.scratch_cards}"
