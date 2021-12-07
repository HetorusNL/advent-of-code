class Solution:
    def __init__(self):
        with open("input.txt") as f:
            self._crabs = [int(i) for i in f.readline().strip().split(",")]
        self._min = min(self._crabs)
        self._max = max(self._crabs)

    def solve(self):
        self.part_1()
        self.part_2()

    def _calc_fuel(self, calc_func):
        fuel = {}
        for i in range(self._min, self._max + 1):
            fuel_for_i = 0
            for crab in self._crabs:
                fuel_for_i += calc_func(i, crab)
            fuel[i] = fuel_for_i
        least_fuel = min(fuel.values())
        return least_fuel

    def part_1(self):
        calc_func = lambda i, crab: abs(i - crab)
        least_fuel = self._calc_fuel(calc_func)
        print(f"least fuel with linear fuel consumption: {least_fuel}")

    def part_2(self):
        calc_func = lambda i, crab: sum(range(abs(i - crab) + 1))
        least_fuel = self._calc_fuel(calc_func)
        print(f"least fuel with increasing fuel consumption: {least_fuel}")


if __name__ == "__main__":
    Solution().solve()
