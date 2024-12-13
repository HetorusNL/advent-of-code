from pathlib import Path
import re

"""
A bit of theory...

============================================================

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

10000000012748 = 26*a + 67*b
10000000012176 = 66*a + 21*b

26*a = 10000000012748 - 67*b

a = 10000000012748/26 - (67/26)*b

10000000012176 = 66*(10000000012748/26 - (67/26)*b) + 21*b

10000000012176 = 66*10000000012748/26 - (67/26*66)*b + 21*b

10000000012176 = 66*10000000012748/26 + (21 - 67/26*66)*b

(21 - 67/26*66)*b = 10000000012176 - 66*10000000012748/26

b = (10000000012176 - 66*10000000012748/26)/(21 - 67/26*66)
-> b = 103199174541.99998

->

26*a = 10000000012748 - 67*b

26*a = 10000000012748 - 67*(103199174541.99998)

a = (10000000012748 - 67*(103199174541.99998)) / 26
-> a = 118679050709.00003

10000000012748 == 26 * 118679050709 + 67 * 103199174542
10000000012176 == 66 * 118679050709 + 21 * 103199174542
"""


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


class Part2:
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
            # adjust for the unit conversion error
            prize = Pos(prize.x + 10000000000000, prize.y + 10000000000000)
            self.claw_machines.append(ClawMachine(button_a, button_b, prize))
            line += 4

    def run_claw_machines(self):
        for claw_machine in self.claw_machines:
            button_a: Pos = claw_machine.button_a
            button_b: Pos = claw_machine.button_b
            prize: Pos = claw_machine.prize
            # solve the linear equations
            solution_b: float = (prize.y - button_a.y * prize.x / button_a.x) / (
                button_b.y - button_b.x / button_a.x * button_a.y
            )
            solution_a: float = (prize.x - button_b.x * solution_b) / button_a.x
            a: int = round(solution_a)
            b: int = round(solution_b)
            # see if these a and b indeed solve the linear equation to the prize
            x_correct = prize.x == button_a.x * a + button_b.x * b
            y_correct = prize.y == button_a.y * a + button_b.y * b
            if x_correct and y_correct:
                self.result += a * 3 + b * 1

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        self.parse_input()
        self.run_claw_machines()

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
