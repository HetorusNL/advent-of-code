from burrow1 import Burrow1
from burrow2 import Burrow2
import re
from typing import List


class Solution:
    def __init__(self):
        self._reset_input("1")

    def _reset_input(self, part):
        with open(f"input{part}.txt") as f:
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
        if part == "1":
            self.burrow: Burrow1 = Burrow1(amphipods)
        else:
            self.burrow: Burrow2 = Burrow2(amphipods)

    def solve(self):
        # self.part_1()
        self._reset_input("2")
        self.part_2()

    def part_1(self):
        energies = self.recurse1(self.burrow, 1)
        print(min(energies))
        print(len(energies))

    def recurse1(self, burrow: Burrow1, depth):
        energies = []
        new_burrows: List[Burrow1] = burrow.simulate()
        for i in range(len(new_burrows)):
            new_burrow = new_burrows[i]
            if depth == 1:
                print(i, "-", len(new_burrows))
            if depth == 2:
                print(" ", i, "-", len(new_burrows))
            if new_burrow._finished:
                energies.append(new_burrow._energy)
                continue
            energies.extend(self.recurse1(new_burrow, depth + 1))
        return energies

    def part_2(self):
        energies = self.recurse2(self.burrow, 1)
        print(min(energies))
        print(len(energies))

    def recurse2(self, burrow: Burrow2, depth):
        min_energy = 1e9
        new_burrows: List[Burrow2] = burrow.simulate()
        for i in range(len(new_burrows)):
            new_burrow = new_burrows[i]
            if depth == 1:
                print(i, "-", len(new_burrows))
            if depth == 2:
                print(" ", i, "-", len(new_burrows))
            if new_burrow._finished:
                if new_burrow._energy < min_energy:
                    print(min_energy)
                min_energy = min(min_energy, new_burrow._energy)
                continue
            if new_burrow._energy > min_energy:
                continue
            min_energy = min(min_energy, self.recurse2(new_burrow, depth + 1))
        return min_energy


if __name__ == "__main__":
    Solution().solve()
