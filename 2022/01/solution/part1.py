from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.elf_calories: list[int] = [0]
        for line in self.lines:
            if line == "":
                self.elf_calories.append(0)
            else:
                self.elf_calories[len(self.elf_calories) - 1] += int(line)
        # calculate the highest (single) number in the list
        self.max_energy = max(self.elf_calories)

    def get_result(self) -> str:
        return f"highest number of calories a single elf is carrying: {self.max_energy} calories"
