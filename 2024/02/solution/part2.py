from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def check_single(self, previous: int, values: list[int], func):
        for value in values:
            if func(value, previous) in [1, 2, 3]:
                previous = value
            else:
                return False
        # all elements processed successfully
        self.result += 1
        return True

    def check_values(self, values: list[int]):
        previous = values.pop(0)
        # test if the sequence is increasing
        func = lambda left, right: left - right
        if self.check_single(previous, values, func):
            return True
        # test if the sequence is decreasing
        func = lambda left, right: right - left
        if self.check_single(previous, values, func):
            return True
        # otherwise the sequence is neither
        return False

    def report_checker(self, values: list[int]):
        # check providing the array as is
        if self.check_values(values.copy()):
            return
        # check with any elements removed as 'Problem Dampener'
        for i in range(len(values)):
            values_copy = values.copy()
            values_copy.pop(i)
            if self.check_values(values_copy.copy()):
                return

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        for line in self.lines:
            values = list(map(int, line.split()))
            self.report_checker(values)

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
