from pathlib import Path


class Common:
    def __init__(self, file: Path):
        with open(file) as f:
            lines = [line.strip() for line in f.readlines()]
        self.lines: list[list[int]] = [list(map(int, line.split(" "))) for line in lines]

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        for sequence in self.lines:
            self.result += self.solve_sequence(sequence)

    def solve_sequence(self, sequence: list[int]) -> int:
        difference = []
        for next_idx in range(1, len(sequence)):
            difference.append(sequence[next_idx] - sequence[next_idx - 1])
        if not all(value == 0 for value in difference):
            self.solve_sequence(difference)
        sequence.append(sequence[-1] + difference[-1])
        return sequence[-1]
