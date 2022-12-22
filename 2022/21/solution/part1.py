from pathlib import Path

from solution.monkey import Monkey
from solution.operation import Operation


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.monkeys: dict[str, Monkey] = {}
        for line in self.lines:
            monkey = Monkey(line)
            self.monkeys[monkey.name] = monkey

        self.root_result = self.get_monkey_result(self.monkeys["root"])

    def get_monkey_result(self, monkey: Monkey) -> int:
        result = monkey.result
        if type(result) is int:
            return result
        elif type(result) is Operation:
            monkey1: Monkey = self.monkeys[result.monkey1]
            monkey1_result: int = self.get_monkey_result(monkey1)
            monkey2: Monkey = self.monkeys[result.monkey2]
            monkey2_result: int = self.get_monkey_result(monkey2)
            return result.resolve(monkey1_result, monkey2_result)
        raise ValueError(f"invalid result type: {type(result)}!")

    def get_result(self) -> str:
        return f"the number that the root monkey calls is: {self.root_result}"
