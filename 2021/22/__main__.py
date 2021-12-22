from cuboid_part_1 import CuboidPart1
from cuboid_part_2 import CuboidPart2
from cuboid_instruction import CuboidInstruction
import re
from typing import List


class Solution:
    def __init__(self):
        self._reset_input()

    def _reset_input(self):
        with open("input.txt") as f:
            lines = [line.strip() for line in f.readlines()]

        regex = (
            r"(?P<state>on|off) x=(?P<xmin>[\-0-9]*)\.\.(?P<xmax>[\-0-9]*)"
            r",y=(?P<ymin>[\-0-9]*)\.\.(?P<ymax>[\-0-9]*)"
            r",z=(?P<zmin>[\-0-9]*)\.\.(?P<zmax>[\-0-9]*)"
        )
        self.cuboid_instructions: List[CuboidInstruction] = []
        for line in lines:
            match_gd = re.match(regex, line).groupdict()
            self.cuboid_instructions.append(CuboidInstruction(match_gd))

    def solve(self):
        self.part_1()
        self._reset_input()
        self.part_2()

    def part_1(self):
        cuboid = CuboidPart1()
        for cuboid_instruction in self.cuboid_instructions:
            cuboid.perform_instruction(cuboid_instruction)
        print(f"number of cubes on after part 1: {cuboid.on_cubes()}")

    def part_2(self):
        cuboids: List[CuboidPart2] = []
        for cuboid_instruction in self.cuboid_instructions:
            new_cuboid = CuboidPart2(cuboid_instruction)
            for cuboid in cuboids:
                cuboid.intersect(cuboid_instruction)
            if cuboid_instruction.state:
                cuboids.append(new_cuboid)
        on_cubes = sum(cuboid.on_cubes() for cuboid in cuboids)
        print(f"number of cubes on after part 2: {on_cubes}")


if __name__ == "__main__":
    Solution().solve()
