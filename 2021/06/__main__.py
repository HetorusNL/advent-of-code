class Solution:
    def __init__(self):
        with open("input.txt") as f:
            _input = f.readline().strip().split(",")
        self.lanternfish_6 = {n: 0 for n in range(7)}
        self.lanternfish_8 = {n: 0 for n in range(9)}
        for n in range(7):
            self.lanternfish_6[n] += _input.count(str(n))

    def solve(self):
        self.part_1(self.lanternfish_6.copy(), self.lanternfish_8.copy())
        self.part_2(self.lanternfish_6.copy(), self.lanternfish_8.copy())

    def part_1(self, lanternfish_6, lanternfish_8):
        # simulate for 80 days and print the result
        for _ in range(80):
            self._simulate(lanternfish_6, lanternfish_8)
        num_lanternfish = self._num_lanternfish(lanternfish_6, lanternfish_8)
        print(f"num lanternfish after 80 days: {num_lanternfish}")

    def part_2(self, lanternfish_6, lanternfish_8):
        # simulate for 256 days and print the result
        for _ in range(256):
            self._simulate(lanternfish_6, lanternfish_8)
        num_lanternfish = self._num_lanternfish(lanternfish_6, lanternfish_8)
        print(f"num lanternfish after 256 days: {num_lanternfish}")

    def _simulate(self, lanternfish_6, lanternfish_8):
        # simulate lanternfish_6
        # each 0-day lanternfish_6 spawns a new lanternfish_6
        new_lanternfish = lanternfish_6[0]
        # update the lanternfish_6 from day 1-6 to 0-5
        for n in range(6):
            lanternfish_6[n] = lanternfish_6[n + 1]

        # simulate lanternfish_8
        # each 0-day lanternfish_8 spawns a new lanternfish_6 and lanternfish_8
        new_lanternfish += lanternfish_8[0]
        # update the lanternfish_8 from day 1-8 to 0-7
        for n in range(8):
            lanternfish_8[n] = lanternfish_8[n + 1]

        # add the 0-day lanternfish_6 and lanternfish_8 to lanternfish_X[X]
        lanternfish_6[6] = new_lanternfish
        lanternfish_8[8] = new_lanternfish

    def _num_lanternfish(self, lanternfish_6, lanternfish_8):
        return sum(lanternfish_6.values()) + sum(lanternfish_8.values())


if __name__ == "__main__":
    Solution().solve()
