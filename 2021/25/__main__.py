from sea_cucumbers import SeaCucumbers
import re
from typing import Dict, List


class Solution:
    def __init__(self):
        self._reset_input()

    def _reset_input(self):
        with open("input.txt") as f:
            lines = [line.strip() for line in f.readlines()]

        self.sc = SeaCucumbers()
        for line in lines:
            self.sc.add_line(line)
        self.sc.print()

    def solve(self):
        self.part_1()
        # self._reset_input()
        # self.part_2()

    def part_1(self):
        num_steps = 0
        while self.sc.step():
            num_steps += 1
        self.sc.print()
        print(f"no sea cucumber moved after step {num_steps + 1}")

    def part_2(self):
        pass


if __name__ == "__main__":
    Solution().solve()
