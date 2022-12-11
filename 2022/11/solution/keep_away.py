import math

from solution.monkey import Monkey


class KeepAway:
    def __init__(self, lines: list[str]):
        self._monkeys: list[Monkey] = []
        monkey_lines = []
        for line in lines:
            if line == "":
                # create new monkey and empty monkey lines
                self._monkeys.append(Monkey(monkey_lines))
                monkey_lines = []
            else:
                monkey_lines.append(line)
        # if there are monkey_lines left, add the last monkey
        if monkey_lines:
            self._monkeys.append(Monkey(monkey_lines))

        # calculate the least common multiple of the monkey division tests
        self._lcm = math.lcm(*[monkey.test_num for monkey in self._monkeys])

    def simulate_rounds(self, rounds: int, divide_worry_level: bool):
        for _ in range(rounds):
            self._simulate_round(divide_worry_level)

    @property
    def monkey_business(self) -> int:
        inspection_counters = [monkey.inspection_counter for monkey in self._monkeys]
        # get the two most active monkeys and return the monkey business (multiplication)
        most_active_monkeys = sorted(inspection_counters)[len(inspection_counters) - 2 :]
        return most_active_monkeys[0] * most_active_monkeys[1]

    def _simulate_round(self, divide_worry_level: bool):
        for monkey in self._monkeys:
            num_items = monkey.num_items
            for item in monkey.items:
                # apply operation to the item
                to_monkey, item = monkey.process(item, divide_worry_level)
                self._monkeys[to_monkey].append_item(item % self._lcm)
            # remove the processed items from the monkey
            monkey.items = monkey.items[num_items:]
