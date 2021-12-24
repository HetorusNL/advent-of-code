from registers import Registers
from typing import Union


class Instruction:
    def __init__(self, op: str, a: str, b: Union[str, None] = None):
        self._ops = {
            "inp": self.inp,
            "add": self.add,
            "mul": self.mul,
            "div": self.div,
            "mod": self.mod,
            "eql": self.eql,
        }
        self.op = self._ops[op]
        self.a = a
        self.b = b

    def execute(self, registers: Registers):
        # extract the operands
        val_a = registers.get(self.a)
        if isinstance(self.b, str):
            try:
                val_b = int(self.b)
            except:
                val_b = registers.get(self.b)
        else:
            val_b = self.b
        # execute the instruction
        res = self.op(val_a, val_b, registers)
        # store the result
        registers.set(self.a, res)

    def inp(self, val_a: int, val_b: int, registers: Registers):
        return registers.get_input()

    def add(self, val_a: int, val_b: int, registers: Registers):
        try:
            val_a + val_b
        except:
            print(val_a, val_b, self.a, self.b, registers.get("w"))
        return val_a + val_b

    def mul(self, val_a: int, val_b: int, registers: Registers):
        return val_a * val_b

    def div(self, val_a: int, val_b: int, registers: Registers):
        assert val_b != 0
        return val_a // val_b

    def mod(self, val_a: int, val_b: int, registers: Registers):
        assert val_b >= 0
        return val_a % val_b

    def eql(self, val_a: int, val_b: int, registers: Registers):
        return 1 if val_a == val_b else 0
