class Solution:
    def __init__(self):
        with open("input.txt") as f:
            self._input = [a.strip() for a in f.readlines()]

    def solve(self):
        self.part_1()
        self.part_2()

    def part_1(self):
        num_bits = len(self._input[0])
        gamma_rate = 0
        for i in range(num_bits):
            gamma_rate *= 2
            d = sum(int(a[i]) for a in self._input)
            gamma_rate += d > len(self._input) // 2
        epsilon_rate = pow(2, num_bits) - 1 - gamma_rate
        print(f"power consumption of submarine: {gamma_rate * epsilon_rate}")

    def part_2(self):
        ogr = self._calc_oxygen_generator_rating(self._input)
        csr = self._calc_co2_scrubber_rating(self._input)
        print(f"life support rating of submarine: {ogr * csr}")

    def _calc_oxygen_generator_rating(self, _input):
        most_common_func = lambda _sum, _half_len: _sum >= _half_len
        return self._calc_rating(_input, most_common_func)

    def _calc_co2_scrubber_rating(self, _input):
        most_common_func = lambda _sum, _half_len: _sum < _half_len
        return self._calc_rating(_input, most_common_func)

    def _calc_rating(self, _input, most_common_func):
        num_bits = len(_input[0])
        for i in range(num_bits):
            _sum = sum(int(a[i]) for a in _input)
            _half_len = len(_input) / 2
            most_common = most_common_func(_sum, _half_len)
            _input = [a for a in _input if int(a[i]) == most_common]
            if len(_input) == 1:
                return int(_input[0], base=2)


if __name__ == "__main__":
    Solution().solve()
