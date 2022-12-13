from enum import Enum
import json


class Order(Enum):
    CORRECT = 1
    INCORRECT = 2
    INDECISIVE = 3


class DistressSignal:
    def __init__(self, left: str, right: str):
        self._left: list = json.loads(left)
        self._right: list = json.loads(right)

    def is_in_right_order(self) -> bool:
        return self._is_in_right_order(self._left, self._right) == Order.CORRECT

    def _is_in_right_order(self, left: list, right: list) -> Order:
        for idx in range(len(right)):
            if idx + 1 > len(left):
                return Order.CORRECT
            elif type(right[idx]) == list and type(left[idx]) == list:
                result = self._is_in_right_order(left[idx], right[idx])
                if result != Order.INDECISIVE:
                    return result
            elif type(right[idx]) == list and type(left[idx]) != list:
                result = self._is_in_right_order([left[idx]], right[idx])
                if result != Order.INDECISIVE:
                    return result
            elif type(right[idx]) != list and type(left[idx]) == list:
                result = self._is_in_right_order(left[idx], [right[idx]])
                if result != Order.INDECISIVE:
                    return result
            elif left[idx] < right[idx]:
                return Order.CORRECT
            elif left[idx] > right[idx]:
                return Order.INCORRECT
        if len(left) > len(right):
            return Order.INCORRECT
        return Order.INDECISIVE
