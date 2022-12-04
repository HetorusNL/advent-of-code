from pathlib import Path

from solution.elf import Elf


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        # find the elven pairs that have overlapping schedules
        self.overlapping_elven_schedules: int = 0
        for line in self.lines:
            elf1, elf2 = Elf.parse_elf_line(line)
            if elf1.overlaps(elf2):
                self.overlapping_elven_schedules += 1

    def get_result(self) -> str:
        message = "the number of elves pairs having overlapping schedules"
        return f"{message}: {self.overlapping_elven_schedules}"
