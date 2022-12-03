from pathlib import Path
import string


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        # find the duplicates in the two compartments
        self.duplicates: list[str] = []
        for line in self.lines:
            for char in line[: len(line) // 2]:
                if char in line[len(line) // 2 :]:
                    self.duplicates.append(char)
                    break

        # for all duplicates calculate the priority
        self.priority = 0
        for duplicate in self.duplicates:
            try:
                priority = string.ascii_lowercase.index(duplicate) + 1
            except ValueError:
                priority = string.ascii_uppercase.index(duplicate) + 27
            self.priority += priority

    def get_result(self) -> str:
        return f"the priority of the compartments common item is: {self.priority}"
