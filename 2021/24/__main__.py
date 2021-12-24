from alu import ALU


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
        for raw_instruction in lines:
            self.alu.add_instruction(raw_instruction)
        # self.alu.print_instructions()

    def solve(self):
        self._reset_input("input.txt")
        self.part_1()
        # self._reset_input("input.txt")
        # self.part_2()

    def part_1(self):
        master_digits = [None] * 14
        for _ in range(7):
            new_digits = master_digits.copy()
            for digit in range(13, -1, -1):
                vals = {}
                for i in range(9, 0, -1):
                    self._reset_input("input.txt")
                    inputs = []
                    for d in range(13, digit, -1):
                        inputs.append(
                            master_digits[d] if master_digits[d] else 9
                        )
                    inputs.append(i)
                    for d in range(digit - 1, -1, -1):
                        inputs.append(
                            master_digits[d] if master_digits[d] else 9
                        )
                    [self.alu.registers.add_input(v) for v in inputs]

                    self.alu.run()
                    vals[i] = self.alu.registers.get("z")
                # print(inputs)
                # print(vals)
                # print(len(set(vals.values())))
                if len(set(vals.values())) == 2:
                    minval = list(vals.keys())[
                        list(vals.values()).index(min(vals.values()))
                    ]
                    print(
                        f"count: {list(vals.values()).count(min(vals.values()))}"
                    )
                    if list(vals.values()).count(min(vals.values())) == 1:
                        new_digits[digit] = minval
                        print("adding minval")
            print(new_digits)
            master_digits = new_digits
        print(master_digits)

        for a in range(9, 0, -1):
            for b in range(9, 0, -1):
                for c in range(9, 0, -1):
                    for d in range(9, 0, -1):
                        inputs = []
                        for i in range(14):
                            if i == 0:
                                inputs.append(a)
                            elif i == 5:
                                inputs.append(b)
                            elif i == 12:
                                inputs.append(c)
                            elif i == 13:
                                inputs.append(d)
                            else:
                                inputs.append(master_digits[i])

                        self._reset_input("input.txt")
                        [self.alu.registers.add_input(v) for v in inputs]
                        self.alu.run()
                        if self.alu.registers.get("z") < 100000:
                            print(self.alu.registers.get("z"))

        found_digits = [None] * 14
        for val in range(10, 0, -1):
            for digit in range(13, -1, -1):
                index = []
                value = []
                for i in range(0, 10):
                    self._reset_input("input.txt")
                    inputs = []
                    for d in range(0, digit):
                        inputs.append(
                            master_digits[d]
                            if master_digits[d]
                            else found_digits[d]
                            if found_digits[d]
                            else val
                        )
                    inputs.append(i)
                    for d in range(digit + 1, 14):
                        inputs.append(
                            master_digits[d]
                            if master_digits[d]
                            else found_digits[d]
                            if found_digits[d]
                            else val
                        )
                    [self.alu.registers.inputs.append(v) for v in inputs]
                    self.alu.run()
                    index.append(i)
                    output = self.alu.registers.get("z")
                    value.append(output)
                found_digits[digit] = index[value.index(min(value))]
            print("".join(str(d) for d in found_digits))
        self._reset_input("input.txt")
        [self.alu.registers.add_input(d) for d in found_digits]
        self.alu.run()
        print(self.alu.registers.get("z"))

    def part_2(self):
        pass


if __name__ == "__main__":
    Solution().solve()
