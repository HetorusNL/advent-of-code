from burrow import Burrow
import re


class Solution:
    def __init__(self):
        self._reset_input()

    def _reset_input(self):
        with open("input.txt") as f:
            lines = [line.strip() for line in f.readlines()]

        amphipods = []
        for line in lines:
            regex = (
                r"(?P<first>[ABCD])#(?P<second>[ABCD])#"
                r"(?P<third>[ABCD])#(?P<fourth>[ABCD])"
            )
            match = re.search(regex, line)
            if not match:
                continue
            gd = match.groupdict()
            amphipod = [gd["first"], gd["second"], gd["third"], gd["fourth"]]
            amphipods.append(amphipod)
        self.burrow: Burrow = Burrow(amphipods)

    def solve(self):
        self.part_1()
        # self._reset_input()
        # self.part_2()

    def part_1(self):
        burrows = self.recurse(self.burrow, 1)
        print(min(b._energy for b in burrows))
        print(len(burrows))

    def recurse(self, burrow: Burrow, depth):
        finished_burrows = []
        new_burrows = burrow.simulate()
        for i in range(len(new_burrows)):
            new_burrow = new_burrows[i]
            if depth == 1:
                print(i, "-", len(new_burrows))
            if depth == 2:
                print(" ", i, "-", len(new_burrows))
            if new_burrow._finished:
                finished_burrows.append(new_burrow)
                continue
            finished_burrows.extend(self.recurse(new_burrow, depth + 1))
        return finished_burrows

    def part_2(self):
        pass


if __name__ == "__main__":
    Solution().solve()
