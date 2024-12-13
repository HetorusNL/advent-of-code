from pathlib import Path
import re


class Pos:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def multiply(self, factor: int) -> "Pos":
        return Pos(self.x * factor, self.y * factor)

    def __add__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y)

    def __mul__(self, factor: int) -> "Pos":
        return Pos(self.x * factor, self.y * factor)

    def __eq__(self, other: object) -> bool:
        assert type(other) == Pos
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"


class ClawMachine:
    def __init__(self, button_a: Pos, button_b: Pos, prize: Pos):
        self.button_a: Pos = button_a
        self.button_b: Pos = button_b
        self.prize: Pos = prize

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"button_a: {self.button_a}, button_b: {self.button_b}, prize: {self.prize}"


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.button_a_regex: str = r"^Button A: X\+(?P<x>[0-9]+), Y\+(?P<y>[0-9]+)$"
        self.button_b_regex: str = r"^Button B: X\+(?P<x>[0-9]+), Y\+(?P<y>[0-9]+)$"
        self.prize_regex: str = r"^Prize: X=(?P<x>[0-9]+), Y=(?P<y>[0-9]+)$"

    def parse_line(self, regex: str, line: int):
        match = re.match(regex, self.lines[line + 0])
        assert match
        group: dict[str, str] = match.groupdict()
        return Pos(int(group["x"]), int(group["y"]))

    def parse_input(self):
        line = 0
        self.claw_machines: list[ClawMachine] = []
        while line < len(self.lines):
            button_a = self.parse_line(self.button_a_regex, line + 0)
            button_b = self.parse_line(self.button_b_regex, line + 1)
            prize = self.parse_line(self.prize_regex, line + 2)
            self.claw_machines.append(ClawMachine(button_a, button_b, prize))
            line += 4

    def run_claw_machines(self):
        for claw_machine in self.claw_machines:
            # for now, just naively brute force the result
            price_list: list[int] = []
            for a in range(101):
                for b in range(101):
                    pos: Pos = claw_machine.button_a * a + claw_machine.button_b * b
                    if claw_machine.prize == pos:
                        price_list.append(a * 3 + b * 1)
            if price_list:
                self.result += min(price_list)

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        self.parse_input()
        self.run_claw_machines()

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
