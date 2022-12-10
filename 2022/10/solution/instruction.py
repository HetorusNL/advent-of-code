import re
from enum import Enum
from typing import Union


class InstrBase:
    def __init__(self, parameters):
        self._parameters: Union[str, None] = parameters

    def run(self, registers: dict[str, int]):
        pass

    @property
    def is_complete(self):
        return True


class InstrNoop(InstrBase):
    def __init__(self, parameters):
        InstrBase.__init__(self, parameters)


class InstrAddx(InstrBase):
    def __init__(self, parameters):
        InstrBase.__init__(self, parameters)
        self._x = int(parameters)
        self._delay = 2

    def run(self, registers: dict[str, int]):
        if self.is_complete:
            return
        self._delay -= 1
        if self._delay <= 0:
            registers["x"] += self._x

    @property
    def is_complete(self):
        return self._delay <= 0


class Instruction:
    def __init__(self, line: str):
        self._instruction = InstrBase(None)
        self._parameters: Union[str, None] = None
        self._parse_instruction(line)

    def _parse_instruction(self, line: str):
        match = re.match(r"^(?P<instruction>[a-zA-Z0-9]*)\s?(?P<parameters>.*)$", line)
        assert match, f"invalid instruction encountered: {line}!"
        parameters = match.groupdict().get("parameters")
        match match["instruction"].lower():
            case "noop":
                self._instruction = InstrNoop(parameters)
            case "addx":
                self._instruction = InstrAddx(parameters)

    def run(self, registers: dict[str, int]):
        self._instruction.run(registers)

    @property
    def is_complete(self):
        return self._instruction.is_complete
