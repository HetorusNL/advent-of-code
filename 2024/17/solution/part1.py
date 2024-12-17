from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def parse_input(self):
        self.reg_a: int = int(self.lines[0].split(":")[1])
        self.reg_b: int = int(self.lines[1].split(":")[1])
        self.reg_c: int = int(self.lines[2].split(":")[1])
        line: str = self.lines[4].split(":")[1].strip()
        self.program: dict[int, int] = {index: int(value) for index, value in enumerate(line.split(","))}
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
        self.result: str = ",".join(map(str, self.output))

    def solve(self) -> None:
        print("solving...")
        self.parse_input()
        self.run()

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
