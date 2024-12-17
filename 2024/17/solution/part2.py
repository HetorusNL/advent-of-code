from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def parse_input(self):
        self.reg_a: int = int(self.lines[0].split(":")[1])
        self.reg_b: int = int(self.lines[1].split(":")[1])
        self.reg_c: int = int(self.lines[2].split(":")[1])
        line: str = self.lines[4].split(":")[1].strip()
        self.program: dict[int, int] = {index: int(value) for index, value in enumerate(line.split(","))}
        self.program_values = list(map(int, line.split(",")))
        self.ip = 0

    def combo(self) -> int:
        match value := self.program[self.ip + 1]:
            case literal if value >= 0 and value <= 3:
                return literal
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c
            case 7:
                # reserved and invalid in a program
                assert False
            case _:
                # invalid
                assert False

    def literal(self) -> int:
        return self.program[self.ip + 1]

    def run(self):
        self.output: list[int] = []
        # run the program
        while self.ip in self.program:
            match self.program[self.ip]:
                case 0:
                    self.reg_a = self.reg_a // (2 ** self.combo())
                case 1:
                    self.reg_b = self.reg_b ^ self.literal()
                case 2:
                    self.reg_b = self.combo() % 8
                case 3:
                    if self.reg_a != 0:
                        self.ip = self.literal()
                        continue  # don't do the IP incremention, but continue
                case 4:
                    self.reg_b = self.reg_b ^ self.reg_c
                case 5:
                    self.output.append(self.combo() % 8)
                case 6:
                    self.reg_b = self.reg_a // (2 ** self.combo())
                case 7:
                    self.reg_c = self.reg_a // (2 ** self.combo())
                case _:
                    assert False
            # advance the IP by 2
            self.ip += 2

    def solve(self) -> None:
        print("solving...")
        # in reverse order the digits matter for the output
        # so calculate a list of magic values to get the program output
        magic_values: list[int] = []
        while True:
            # construct the initial value, all digits except the last
            initial_value: int = 0
            for digit in magic_values:
                initial_value *= 8
                initial_value += digit
            # compute the next digit, should be [0-7]
            for next_magic_value in range(8):
                self.parse_input()
                self.reg_a = initial_value * 8 + next_magic_value
                self.run()
                # match the current subset of output values
                last_output_values: list[int] = self.output[-len(magic_values) - 1 :]
                last_program_values: list[int] = self.program_values[-len(magic_values) - 1 :]
                # check if we found the whole output, then set the result and return
                if self.output == self.program_values:
                    self.result: int = initial_value * 8 + next_magic_value
                    return
                # if we found a subset of the program, we got the next digit, onto the next
                if last_output_values == last_program_values:
                    magic_values.append(next_magic_value)
                    break
            else:
                # next digit not found!
                assert False

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
