from pathlib import Path


class Part2:
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
        # calculate the sum of the highest X values in the list
        self.num_highest_values = 3
        num_elfs = len(self.elf_calories)
        self.top_three_calories = sum(sorted(self.elf_calories)[num_elfs - self.num_highest_values :])

    def get_result(self) -> str:
        return (
            f"number of calories that the top {self.num_highest_values} elfs are carrying: "
            f"{self.top_three_calories} calories"
        )
