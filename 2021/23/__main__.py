from burrow1 import Burrow1
from burrow2 import Burrow2
import re
from typing import List


class Solution:
    def __init__(self):
        self._reset_input("input1.txt")

    def _reset_input(self, filename):
        with open(filename) as f:
            lines = [line.strip() for line in f.readlines()]

        amphipods = []
        self.cache = {}
        self.min_energy = 1e9
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
        if "2" in filename:
            self.burrow: Burrow2 = Burrow2(amphipods)
        else:
            self.burrow: Burrow1 = Burrow1(amphipods)

    def solve(self):
        self.part_1()
        self._reset_input("input2.txt")
        self.part_2()

    def part_1(self):
        self.recurse1(self.burrow)
        energy = self.min_energy
        print(f"lowest energy required to move 2 rows of amphipods: {energy}")

    def recurse1(self, burrow: Burrow1):
        new_burrows: List[Burrow1] = burrow.simulate()
        for i in range(len(new_burrows)):
            new_burrow = new_burrows[i]
            _hash = hash(new_burrow)
            if _hash in self.cache:
                continue
            self.cache[_hash] = True
            if new_burrow.finished:
                self.min_energy = min(self.min_energy, new_burrow._energy)
                continue
            self.recurse1(new_burrow)

    def part_2(self):
        self.recurse2(self.burrow)
        energy = self.min_energy
        print(f"lowest energy required to move 4 rows of amphipods: {energy}")

    def recurse2(self, burrow: Burrow2):
        new_burrows: List[Burrow2] = burrow.simulate()
        for i in range(len(new_burrows)):
            new_burrow = new_burrows[i]
            _hash = hash(new_burrow)
            if _hash in self.cache:
                continue
            self.cache[_hash] = True
            if new_burrow.finished:
                self.min_energy = min(self.min_energy, new_burrow._energy)
                continue
            if new_burrow._energy > self.min_energy:
                continue
            self.recurse2(new_burrow)


if __name__ == "__main__":
    Solution().solve()
