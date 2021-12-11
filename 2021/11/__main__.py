from coord import Coord
from typing import List


class Solution:
    def __init__(self):
        self._reset_input()

    def _reset_input(self):
        # the octopusses
        self._op = []

        with open("input.txt") as f:
            lines = f.readlines()

        for line in lines:
            self._op.append([int(op) for op in line.strip()])

        self.w = len(self._op[0])
        self.h = len(self._op)

    def solve(self):
        self.part_1()
        self._reset_input()
        self.part_2()

    def part_1(self):
        flashed_ops = 0
        for i in range(100):
            flashed_ops += self._simulate()
        print(f"octopus flashes after 100 simulations: {flashed_ops}")

    def part_2(self):
        simulation = 0
        while True:
            simulation += 1
            flashed_ops = self._simulate()
            if flashed_ops == self.w * self.h:
                break
        print(f"octopus flash simultaneously after {simulation} simulations")

    def _print(self):
        for line in self._op:
            print(line)
        print()

    def _simulate(self):
        ready_to_flash_ops = self._increment_ops()
        flashed_ops = self._flash_ops(ready_to_flash_ops)
        self._reset_flashed_ops(flashed_ops)
        return len(flashed_ops)

    def _increment_ops(self):
        ready_to_flash_ops = []
        for y in range(self.h):
            for x in range(self.w):
                self._op[y][x] += 1
                if self._op[y][x] > 9:
                    ready_to_flash_ops.append(Coord(x, y))
        return ready_to_flash_ops

    def _flash_ops(self, ready_to_flash_ops: List[Coord]):
        index = 0
        while index < len(ready_to_flash_ops):
            # loop through its adjacent coords and find if they should flash
            ac = ready_to_flash_ops[index].adjacent_coords(self.w, self.h)
            for coord in ac:
                self._op[coord.y][coord.x] += 1
                if self._op[coord.y][coord.x] > 9:
                    if coord not in ready_to_flash_ops:
                        ready_to_flash_ops.append(coord)
            index += 1
        return ready_to_flash_ops

    def _reset_flashed_ops(self, flashed_ops: List[Coord]):
        for coord in flashed_ops:
            if self._op[coord.y][coord.x] > 9:
                self._op[coord.y][coord.x] = 0


if __name__ == "__main__":
    Solution().solve()
