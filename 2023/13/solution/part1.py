from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.patterns: list[list[str]] = []
        self.patterns.append([])
        for line in self.lines:
            if line:
                self.patterns[-1].append(line)
            else:
                self.patterns.append([])

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        for pattern in self.patterns:
            self.solve_pattern(pattern)

    def solve_pattern(self, pattern: list[str]):
        # test column reflection
        height = len(pattern)
        width = len(pattern[0])
        for col_idx in range(width - 1):
            if all(pattern[row_idx][col_idx] == pattern[row_idx][col_idx + 1] for row_idx in range(height)):
                # test if more to the top or bottom
                is_reflection = True
                if col_idx + 1 < width / 2:
                    for test_col_idx in range(col_idx):
                        if any(
                            pattern[row_idx][test_col_idx] != pattern[row_idx][2 * col_idx + 1 - test_col_idx]
                            for row_idx in range(height)
                        ):
                            is_reflection = False
                else:
                    for test_col_idx in range(col_idx, width):
                        if any(
                            pattern[row_idx][test_col_idx] != pattern[row_idx][col_idx - (test_col_idx - col_idx) + 1]
                            for row_idx in range(height)
                        ):
                            is_reflection = False
                if is_reflection:
                    self.result += col_idx + 1
        # test row reflection
        for row_idx in range(height - 1):
            if pattern[row_idx] == pattern[row_idx + 1]:
                # test if more to the right or left
                is_reflection = True
                if row_idx + 1 < height / 2:
                    for test_row_idx in range(row_idx):
                        if pattern[test_row_idx] != pattern[2 * row_idx + 1 - test_row_idx]:
                            is_reflection = False
                            break
                else:
                    for test_row_idx in range(row_idx + 1, height):
                        if pattern[test_row_idx] != pattern[row_idx - (test_row_idx - row_idx) + 1]:
                            is_reflection = False
                            break
                if is_reflection:
                    self.result += 100 * (row_idx + 1)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
