from alu import ALU
import re
from typing import Dict, List


class Solution:
    def __init__(self):
        self._run_tests()

    def _run_tests(self):
        self._reset_input("test1_input.txt")
        self.alu.registers.add_input(10)
        self.alu.run()
        assert self.alu.registers.get("x") == -10

        self._reset_input("test2_input.txt")
        self.alu.registers.add_input(2).add_input(6)
        self.alu.run()
        assert self.alu.registers.get("z") == 1

        self._reset_input("test2_input.txt")
        self.alu.registers.add_input(2).add_input(5)
        self.alu.run()
        assert self.alu.registers.get("z") == 0

        self._reset_input("test3_input.txt")
        self.alu.registers.add_input(10)
        self.alu.run()
        assert self.alu.registers.get("w") == 1
        assert self.alu.registers.get("x") == 0
        assert self.alu.registers.get("y") == 1
        assert self.alu.registers.get("z") == 0

    def _reset_input(self, file):
        with open(file) as f:
            lines = [line.strip() for line in f.readlines()]

        self.alu = ALU()
        self.z_targets = []
        for raw_instruction in lines:
            match = re.match(r"add x (?P<num>[\-0-9]{1,})", raw_instruction)
            self.alu.add_instruction(raw_instruction)

            if match:
                if "add x -" in raw_instruction:
                    self.z_targets.append(-int(match.groupdict()["num"]))
                else:
                    self.z_targets.append(None)
        # self.alu.print_instructions()

    def solve(self):
        self._reset_input("input.txt")
        self.part_1()
        self._reset_input("input.txt")
        self.part_2()

    def part_1(self):
        result = self._run_part(range(9, 0, -1))
        print(f"largest model number accepted by MONAD: {result}")

    def part_2(self):
        result = self._run_part(range(1, 10))
        print(f"smallest model number accepted by MONAD: {result}")

    def _run_part(self, range_func: range):
        results: Dict[int, List] = {}
        # loop through the first block
        for i in range_func:
            self.alu.reset()
            self.alu.registers.add_input(i)
            self.alu.run()
            z = self.alu.registers.get("z")
            results[z] = [i]
        # loop through the remaining 13 blocks
        for block in range(1, 14):
            prev = results
            results = {}
            z_target = self.z_targets[block]
            for w in range_func:
                for prev_z in prev:
                    if z_target and prev_z % 26 - z_target != w:
                        continue
                    self.alu.reset()
                    for val in prev[prev_z]:
                        self.alu.registers.add_input(val)
                    self.alu.registers.add_input(w)
                    self.alu.run()
                    z = self.alu.registers.get("z")
                    if z not in results:
                        results[z] = prev[prev_z].copy()
                        results[z].append(w)
        return "".join(str(w) for w in results[0])


if __name__ == "__main__":
    Solution().solve()
