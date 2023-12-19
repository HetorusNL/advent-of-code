from copy import deepcopy

from solution.part import Part
from solution.part_range import PartRange


class Rule:
    def __init__(self, parameter: str | None, operator: str | None, value: str | None, next: str):
        self.parameter = parameter
        self.operator = operator
        self.value = int(value) if value else 0
        self.next = next

    def apply(self, part: Part) -> str | None:
        if self.parameter is None and self.operator is None and self.value == 0:
            return self.next
        else:
            assert self.parameter and self.operator and self.value
            match self.operator:
                case "<":
                    return self.next if part.values[self.parameter] < self.value else None
                case ">":
                    return self.next if part.values[self.parameter] > self.value else None
                case _:
                    assert False

    def get_part_ranges(self, part_range: PartRange) -> tuple[PartRange, str, PartRange | None]:
        if not self.operator:
            return part_range, self.next, None
        assert self.parameter is not None
        pass_part_range = deepcopy(part_range)
        fail_part_range = deepcopy(part_range)
        match self.operator:
            case "<":
                pass_part_range.values[self.parameter]["max"] = self.value - 1
                fail_part_range.values[self.parameter]["min"] = self.value
            case ">":
                pass_part_range.values[self.parameter]["min"] = self.value + 1
                fail_part_range.values[self.parameter]["max"] = self.value
            case _:
                assert False
        return pass_part_range, self.next, fail_part_range
