from pair import Pair
import json


class Solution:
    def __init__(self):
        self._reset_input()

    def _reset_input(self):
        with open("input.txt") as f:
            lines = [line.strip() for line in f.readlines()]

        self.raw_pairs = []
        for line in lines:
            self.raw_pairs.append(json.loads(line))

    def _make_pair(self, line):
        left = line[0]
        right = line[1]
        if isinstance(left, list):
            left = self._make_pair(left)
        if isinstance(right, list):
            right = self._make_pair(right)
        return Pair(left, right)

    def solve(self):
        self.part_1()
        self._reset_input()
        self.part_2()

    def part_1(self):
        new_pair = self._make_pair(self.raw_pairs[0])
        for raw_pair in self.raw_pairs[1:]:
            new_pair = Pair(new_pair, self._make_pair(raw_pair)).reduce()
        print(f"magnitude of the final sum: {new_pair.get_magnitude()}")

    def part_2(self):
        max_magnitude = 0
        for x in range(len(self.raw_pairs)):
            for y in range(len(self.raw_pairs)):
                if x == y:
                    continue
                pair = Pair(
                    self._make_pair(self.raw_pairs[x]),
                    self._make_pair(self.raw_pairs[y]),
                ).reduce()
                max_magnitude = max(max_magnitude, pair.get_magnitude())
        print(f"max magnitude when adding any 2 values: {max_magnitude}")


if __name__ == "__main__":
    Solution().solve()
