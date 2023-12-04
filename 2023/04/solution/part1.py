from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.score = 0
        for line in self.lines:
            line = line.split(":")[1].strip()
            winning, your = line.split("|")
            winning = [winning for winning in winning.split(" ") if winning]
            your = [your for your in your.split(" ") if your]

            good_numbers = 0
            for number in your:
                if number in winning:
                    good_numbers += 1
            if good_numbers:
                self.score += 2 ** (good_numbers - 1)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.score}"
