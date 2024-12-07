from enum import auto
from enum import Enum
from pathlib import Path


class Operation(Enum):
    ADD = auto()
    MUL = auto()


class Equation:
    def __init__(self, result: int, numbers: list[int]):
        self.result = result
        self.numbers = numbers
        self.solved = False


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

        self.equations: list[Equation] = []
        for line in self.lines:
            result, numbers = line.split(":")
            int_numbers: list[int] = list(map(int, numbers.strip().split(" ")))
            self.equations.append(Equation(int(result.strip()), int_numbers))

    def solve_single(self, left: int, right: list[int], operation: Operation, equation: Equation):
        match operation:
            case Operation.ADD:
                left += right.pop(0)
            case Operation.MUL:
                left *= right.pop(0)
        if right:
            # recurse into the solve function
            self.solve_single(left, right.copy(), Operation.ADD, equation)
            self.solve_single(left, right.copy(), Operation.MUL, equation)
        else:
            # the last one, after this the equation is solved
            if left == equation.result:
                equation.solved = True

    def solve_equation(self, equation: Equation):
        left = equation.numbers.pop(0)
        self.solve_single(left, equation.numbers.copy(), Operation.ADD, equation)
        self.solve_single(left, equation.numbers.copy(), Operation.MUL, equation)

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        for equation in self.equations:
            self.solve_equation(equation)
            if equation.solved:
                self.result += equation.result

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
