class Solution:
    def __init__(self):
        with open("input.txt") as f:
            self._input = [int(a.strip()) for a in f.readlines()]

    def solve(self):
        self.part_1()
        self.part_2()

    def part_1(self):
        length = len(self._input) - 1
        inc = sum(self._input[i + 1] > self._input[i] for i in range(length))
        print(f"number of times a depth measurement increases: {inc}")

    def part_2(self):
        window_func = lambda i: sum(self._input[i : i + 3])
        window = [window_func(i) for i in range(len(self._input) - 2)]
        length = len(window) - 1
        inc = sum(window[i + 1] > window[i] for i in range(length))
        print(f"number of times a windowed depth measurement increases: {inc}")


if __name__ == "__main__":
    Solution().solve()
