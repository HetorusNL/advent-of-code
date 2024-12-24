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


class Part2:
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

    def solve(self) -> None:
        print("solving...")
        self.parse_input()
        output_regex = re.compile(r"z[0-9]{2}")
        input_regex = re.compile(r"[xy][0-9]{2}")
        # several checks to make sure that the adder is correct
        # the output of AND gates should always be OR, except for the first
        faulty_operations: dict[Operation, bool] = {}
        for operation in self.operations:
            if operation.in1 in ["x00", "y00"]:
                continue
            if operation.op_str == "AND":
                for next_operation in self.operations:
                    if operation.out == next_operation.in1 or operation.out == next_operation.in2:
                        if next_operation.op_str != "OR":
                            faulty_operations[operation] = True
                            break
        # XOR gate should always go to XOR, AND or outputs
        for operation in self.operations:
            if operation.op_str == "XOR":
                # test if it's an output
                if re.match(output_regex, operation.out):
                    continue
                # otherwise, the output must be an XOR or AND gate
                for next_operation in self.operations:
                    if operation.out == next_operation.in1 or operation.out == next_operation.in2:
                        if next_operation.op_str not in ["XOR", "AND"]:
                            faulty_operations[operation] = True
                            break
        # outputs should always be generated by an XOR (except the last one)
        num_z_values: int = len([wire for wire in self.wires.keys() if re.match(output_regex, wire)])
        for operation in self.operations:
            if re.match(output_regex, operation.out):
                # ignore the last one
                if operation.out == f"z{num_z_values-1:02}":
                    continue
                if operation.op_str != "XOR":
                    faulty_operations[operation] = True
        # OR gates should always go to XOR or AND gates
        for operation in self.operations:
            if operation.op_str == "OR":
                for next_operation in self.operations:
                    if operation.out == next_operation.in1 or operation.out == next_operation.in2:
                        if next_operation.op_str not in ["XOR", "AND"]:
                            faulty_operations[operation] = True
                            break
        # carry values should always go to AND or OR
        for operation in self.operations:
            if re.match(output_regex, operation.out):
                continue
            if re.match(input_regex, operation.in1) or re.match(input_regex, operation.in2):
                continue
            if operation.op_str not in ["AND", "OR"]:
                faulty_operations[operation] = True

        self.result: str = ",".join(sorted(operation.out for operation in faulty_operations))

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
