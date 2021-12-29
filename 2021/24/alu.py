from instruction import Instruction
from registers import Registers
from typing import List


class ALU:
    def __init__(self):
        self.registers = Registers()
        self.instructions: List[Instruction] = []

    def reset(self):
        self.registers.reset()

    def add_instruction(self, raw_instruction: str):
        parts = [part.strip() for part in raw_instruction.split(" ")]
        self.instructions.append(Instruction(*parts))

    def print_instructions(self):
        for ins in self.instructions:
            has_b = ins.b is not None
            print(f"{ins.op} {ins.a} {ins.b if has_b else ''}")

    def run(self, verbose=False):
        for ins in self.instructions:
            try:
                ins.execute(self.registers)
            except:
                ins_number = self.instructions.index(ins)
                if verbose:
                    print(f"crashed on instruction {ins_number}")
                return
