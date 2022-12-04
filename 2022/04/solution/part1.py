from pathlib import Path

from solution.elf import Elf


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        # find the elven pairs that have a schedule fully contain in the other
        self.fully_contain_elves_schedules: int = 0
        for line in self.lines:
            elf1, elf2 = Elf.parse_elf_line(line)
            if elf1.fully_contains(elf2):
                self.fully_contain_elves_schedules += 1

    def get_result(self) -> str:
        message = "the number of elves having its schedule fully contained in the other"
        return f"{message}: {self.fully_contain_elves_schedules}"
