from seven_segment import SevenSegment


class Solution:
    def __init__(self):
        self._signal_patterns = []
        self._output_values = []

        with open("input.txt") as f:
            lines = f.readlines()

        for line in lines:
            (pattern, values) = line.strip().split("|")
            self._signal_patterns.append(pattern.strip().split(" "))
            self._output_values.append(values.strip().split(" "))

    def solve(self):
        self.part_1()
        self.part_2()

    def part_1(self):
        num_1_4_7_8 = 0
        for ov in self._output_values:
            num_1_4_7_8 += sum(len(o) in [2, 4, 3, 7] for o in ov)
        print(f"number of times 1 4 7 8 appears in output: {num_1_4_7_8}")

    def part_2(self):
        output_value_sum = 0
        for i in range(len(self._signal_patterns)):
            seven_segment = SevenSegment(self._signal_patterns[i])
            number = 0
            for in_digit in self._output_values[i]:
                number *= 10
                number += seven_segment.get_number(in_digit)
            output_value_sum += number
        print(f"sum of all output values: {output_value_sum}")


if __name__ == "__main__":
    Solution().solve()
