from pathlib import Path
import re
from typing import Callable


class Operation:
    def __init__(self, in1: str, op: str, in2: str, out: str):
        self.in1: str = in1
        self.in2: str = in2
        self.out: str = out
        self.op_str: str = op
        match op:
            case "AND":
                self.op: Callable[[int, int], int] = self._and
            case "OR":
                self.op: Callable[[int, int], int] = self._or
            case "XOR":
                self.op: Callable[[int, int], int] = self._xor
            case _:
                assert False

    def apply(self, wires: dict[str, int]):
        wires[self.out] = self.op(wires[self.in1], wires[self.in2])

    def _and(self, in1: int, in2: int) -> int:
        return in1 and in2

    def _or(self, in1: int, in2: int) -> int:
        return in1 or in2

    def _xor(self, in1: int, in2: int) -> int:
        return in1 ^ in2

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"[{self.in1} {self.op_str} {self.in2} -> {self.out}]"


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def parse_input(self):
        self.inputs: dict[str, int] = {}
        self.wires: dict[str, int] = {}
        self.operations: list[Operation] = []
        # precomile the initial values regex
        initial_regex: re.Pattern[str] = re.compile(r"(?P<wire>[a-z][a-z0-9]{2}): (?P<initial>[01])")
        # construct and precompile the operation regex
        in1_re: str = r"(?P<in1>[a-z][a-z0-9]{2})"
        op_re: str = r"(?P<op>AND|OR|XOR)"
        in2_re: str = r"(?P<in2>[a-z][a-z0-9]{2})"
        out_re: str = r"(?P<out>[a-z][a-z0-9]{2})"
        operation_regex: re.Pattern[str] = re.compile(f"{in1_re} {op_re} {in2_re} -> {out_re}")
        # use regex to match all lines
        for line in self.lines:
            # match the initial values
            if match := re.match(initial_regex, line):
                gd = match.groupdict()
                assert type(gd) == dict
                wire: str = gd["wire"]
                initial: str = gd["initial"]
                assert wire not in self.inputs
                self.inputs[wire] = int(initial)
                self.wires[wire] = int(initial)
                continue
            # match the operations
            if match := re.match(operation_regex, line):
                gd = match.groupdict()
                assert type(gd) == dict
                assert type(gd["in1"]) == str and type(gd["in2"]) == str and type(gd["out"]) == str
                in1: str = gd["in1"]
                op: str = gd["op"]
                in2: str = gd["in2"]
                out: str = gd["out"]
                self.operations.append(Operation(in1, op, in2, out))
                # also add the inputs/outputs to the wires dict if not already there
                if in1 not in self.wires:
                    self.wires[in1] = False
                if in2 not in self.wires:
                    self.wires[in2] = False
                if out not in self.wires:
                    self.wires[out] = False
                continue
            # only empty lines should be available
            assert not line
        # ensure we don't have invalid input
        for operation in self.operations:
            assert operation.out not in self.inputs

    def sort_input(self):
        # prepare the inputs for the function
        resolved_inputs: dict[str, bool] = {key: True for key in self.inputs.keys()}
        resolved_operations: list[Operation] = []
        remaining_operations: list[Operation] = self.operations.copy()
        # loop through the remaining operations, and every cycle get an operation that can be resolved
        while remaining_operations:
            operation_index: int = 0
            while operation_index < len(remaining_operations):
                operation: Operation = remaining_operations[operation_index]
                if operation.in1 in resolved_inputs and operation.in2 in resolved_inputs:
                    # this operation is already fully resolved, add to resolved inputs
                    resolved_inputs[operation.out] = True
                    # remove from remaining list and add to resolved list
                    resolved_operations.append(remaining_operations.pop(operation_index))
                    # don't increment the operation_index, as we removed an element
                else:
                    # operation not (yet) resolvable, continue to next
                    operation_index += 1
        assert len(self.operations) == len(resolved_operations)
        self.operations = resolved_operations

    def run_circuit(self):
        # we can now simply apply all operations in order
        for operation in self.operations:
            operation.apply(self.wires)

    def solve(self) -> None:
        print("solving...")
        self.parse_input()
        self.sort_input()
        self.run_circuit()
        output_regex = re.compile(r"z[0-9]{2}")
        keys: list[str] = sorted([wire for wire in self.wires.keys() if re.match(output_regex, wire)], reverse=True)
        self.result: int = int("".join(str(self.wires[out]) for out in keys), 2)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
