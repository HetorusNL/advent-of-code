from typing import Union


class Operation:
    def __init__(self, monkey1: str, monkey2: str, op: str):
        self._monkey1: str = monkey1
        self._monkey2: str = monkey2
        self._op: str = op
        self._monkey1_result: Union[int, None] = None
        self._monkey2_result: Union[int, None] = None

    @property
    def monkey1(self) -> str:
        return self._monkey1

    @property
    def monkey2(self) -> str:
        return self._monkey2

    @property
    def op(self) -> str:
        return self._op

    @op.setter
    def op(self, _op: str):
        self._op = _op

    def resolve(self, monkey1_value: int, monkey2_value: int) -> int:
        match self._op:
            case "+":
                return monkey1_value + monkey2_value
            case "-":
                return monkey1_value - monkey2_value
            case "*":
                return monkey1_value * monkey2_value
            case "/":
                return monkey1_value // monkey2_value
            case "=":
                return monkey1_value - monkey2_value
        raise ValueError(f"invalid op: {self._op}!")
