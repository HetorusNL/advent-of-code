from pathlib import Path
import string


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        # find the common badge between sets of 3 lines
        self.badges: list[str] = []
        while self.lines:
            # extract 3 lines from self.lines
            lines = self.lines[:3]
            self.lines = self.lines[3:]
            badges = list(set(lines[0]))
            # loop through the lines checking if a char exists in all three
            for line in lines[1:]:
                new_badges = []
                for char in badges:
                    if char in line:
                        new_badges.append(char)
                badges = new_badges
            # at this point we can only have 1 badge, otherwise input broken
            assert len(badges) == 1
            self.badges.append(badges[0])

        # for all duplicates calculate the priority
        self.priority = 0
        for badge in self.badges:
            try:
                priority = string.ascii_lowercase.index(badge) + 1
            except ValueError:
                priority = string.ascii_uppercase.index(badge) + 27
            self.priority += priority

    def get_result(self) -> str:
        return f"the priority of the badge of three lines is: {self.priority}"
