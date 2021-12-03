from submarine1 import Submarine1
from submarine2 import Submarine2


class Solution:
    def __init__(self):
        with open("input.txt") as f:
            self._input = [a.strip() for a in f.readlines()]

    def solve(self):
        self.part_1()
        self.part_2()

    def part_1(self):
        sub = Submarine1()
        sub.run_program(self._input)
        print(f"final value: {sub.final_value()}")

    def part_2(self):
        sub = Submarine2()
        sub.run_program(self._input)
        print(f"final value: {sub.final_value()}")


if __name__ == "__main__":
    Solution().solve()
