from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def parse_input(self):
        # add trailing newline to make parsing easier
        self.lines.append("")
        self.keys: list[list[int]] = []
        self.locks: list[list[int]] = []
        first_line: bool = True
        heights: list[int] = [-1, -1, -1, -1, -1]  # don't count the upper/loewr row
        is_key: bool = True
        for line in self.lines:
            # in the first line, locks start with "#" and keys with "."
            if first_line:
                is_key = line[0] == "."
                first_line = False
            if line:
                # add to the heights of the columns
                for index, value in enumerate(line):
                    heights[index] += 1 if value == "#" else 0
            else:
                # prepare for the next line and process the current,
                # also last lock/key is processed because of the trailing newline
                first_line = True
                if is_key:
                    self.keys.append(heights)
                else:
                    self.locks.append(heights)
                heights = [-1, -1, -1, -1, -1]

    def test_locks(self):
        for key in self.keys:
            for lock in self.locks:
                for index in range(len(key)):
                    # if any column doesn't fit, break
                    if key[index] + lock[index] > 5:
                        break
                else:
                    # otherwise the key and lock fit without overlapping
                    self.result += 1

    def solve(self) -> None:
        print("solving...")
        self.result: int = 0
        self.parse_input()
        self.test_locks()

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
