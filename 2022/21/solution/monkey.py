import re
from typing import Union

from solution.operation import Operation


class Monkey:
    def __init__(self, line: str):
        number_regex = r"^(?P<name>[a-z]{4}): (?P<number>[0-9]*)$"
        operation_regex = r"^(?P<name>[a-z]{4}): (?P<monkey1>[a-z]{4}) (?P<op>[+\-*/]) (?P<monkey2>[a-z]{4})$"
        self._result: Union[int, Operation]
        if number_match := re.match(number_regex, line):
            self._name: str = number_match["name"]
            self._result = int(number_match["number"])
        elif operation_match := re.match(operation_regex, line):
            self._name: str = operation_match["name"]
            self._result = Operation(operation_match["monkey1"], operation_match["monkey2"], operation_match["op"])
        else:
            raise ValueError(f"invalid line supplied: {line}!")

    @property
    def name(self) -> str:
        return self._name

    @property
    def result(self) -> Union[int, Operation]:
        return self._result

    @result.setter
    def result(self, result: int):
        self._result = result

    def resolve(self, monkey1_value: int, monkey2_value: int) -> int:
        assert type(self._result) is Operation
        self._result = self._result.resolve(monkey1_value, monkey2_value)
        return self._result
