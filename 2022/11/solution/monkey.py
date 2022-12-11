import re
from typing import Union


class Monkey:
    def __init__(self, lines):
        # extract monkey num
        match = re.match(r"^Monkey (?P<num>[0-9]*):$", lines[0])
        assert match, f"invalid monkey line {lines[0]}!"
        self._num: int = int(match["num"])
        # extract starting items
        match = re.match(r"^Starting items: (?P<items>[0-9, ]*)$", lines[1])
        assert match, f"invalid monkey line {lines[1]}!"
        self._items: list[int] = [int(item.strip()) for item in match["items"].split(",")]
        # extract the operation
        regex = r"^Operation: new = (?P<param1>(old|[0-9]*)) (?P<operator>[*+]) (?P<param2>(old|[0-9]*))$"
        match = re.match(regex, lines[2])
        assert match, f"invalid monkey line {lines[2]}!"
        self._param1: Union[str, int] = match["param1"] if match["param1"] == "old" else int(match["param1"])
        self._operator: str = match["operator"]
        self._param2: Union[str, int] = match["param2"] if match["param2"] == "old" else int(match["param2"])
        # extract the test
        match = re.match(r"^Test: divisible by (?P<num>[0-9]*)$", lines[3])
        assert match, f"invalid monkey line {lines[3]}!"
        self._test_num: int = int(match["num"])
        # extract the true monkey
        match = re.match(r"^If true: throw to monkey (?P<num>[0-9]*)$", lines[4])
        assert match, f"invalid monkey line {lines[4]}!"
        self._monkey_true = int(match["num"])
        # extract the false monkey
        match = re.match(r"^If false: throw to monkey (?P<num>[0-9]*)$", lines[5])
        assert match, f"invalid monkey line {lines[5]}!"
        self._monkey_false = int(match["num"])

        # initialize some other variables
        self._inspection_counter: int = 0

    @property
    def items(self) -> list[int]:
        return self._items

    @items.setter
    def items(self, _items: list[int]):
        self._items = _items

    def append_item(self, items: int):
        self._items.append(items)

    @property
    def num_items(self) -> int:
        return len(self.items)

    @property
    def test_num(self) -> int:
        return self._test_num

    @property
    def inspection_counter(self) -> int:
        return self._inspection_counter

    def process(self, item: int, divide_worry_level: bool) -> tuple[int, int]:
        # increment the inspection counter
        self._inspection_counter += 1
        # apply the operation on the item
        item = self._do_operation(item)
        # divide (and floor) the resulting item by 3
        if divide_worry_level:
            item = item // 3
        # return the true or false value based on the test
        if item % self._test_num == 0:
            return self._monkey_true, item
        else:
            return self._monkey_false, item

    def _do_operation(self, item: int) -> int:
        # perform operation on item
        param1 = item if self._param1 == "old" else self._param1
        param2 = item if self._param2 == "old" else self._param2
        assert type(param1) is int and type(param2) is int, f"invalid params {param1}, {param2}!"
        match self._operator:
            case "+":
                return param1 + param2
            case "*":
                return param1 * param2
        raise AssertionError(f"invalid operator {self._operator}!")
