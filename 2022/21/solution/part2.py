from pathlib import Path

from solution.monkey import Monkey
from solution.operation import Operation


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.current_value: int = 0
        while True:
            self.monkeys: dict[str, Monkey] = {}
            for line in self.lines:
                monkey = Monkey(line)
                self.monkeys[monkey.name] = monkey
            # hack the value of monkey 'humn' to 'current_value'
            self.monkeys["humn"].result = self.current_value
            # we're going to use '-' instead of '=' and it's correct when it returns 0
            # hack the operation of monkey 'root' to '-'
            root: Monkey = self.monkeys["root"]
            assert type(root.result) is Operation
            root.result.op = "-"

            self.root_result = self.get_monkey_result(self.monkeys["root"])
            if self.root_result == 0:
                break
            # we know the value is decreasing (in this input), so use this ginormous speedup
            # it seems that we need to have the lowest possible value,
            # so keep the speedup value relatively high
            if self.root_result > 100:
                self.current_value += self.root_result // 100
            else:
                assert self.root_result >= 0, f"too low speedup value, overshooting target!"
                self.current_value += 1

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
        return f"the value of humn should be: {self.current_value}"
