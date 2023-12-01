from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

        self.lut = {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }
        self.options = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        ]

    def solve(self) -> None:
        print("solving...")
        values = []
        for line in self.lines:
            start = self.get_start(line)
            end = self.get_end(line)
            values.append(int(start + end))
        self.result = sum(values)

    def get_start(self, line: str):
        start_line = line
        while start_line:
            for option in self.options:
                if start_line.startswith(option):
                    return self.lut.get(option, option)
            start_line = start_line[1:]
        assert False

    def get_end(self, line: str):
        end_line = line
        while end_line:
            for option in self.options:
                if end_line.endswith(option):
                    return self.lut.get(option, option)
            end_line = end_line[: len(end_line) - 1]
        assert False

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
