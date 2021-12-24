from instruction import Instruction
from registers import Registers
from typing import List


class ALU:
    def __init__(self):
        self.registers = Registers()
        self.instructions: List[Instruction] = []

    def add_instruction(self, raw_instruction: str):
        parts = [part.strip() for part in raw_instruction.split(" ")]
        self.instructions.append(Instruction(*parts))

    def print_instructions(self):
        for ins in self.instructions:
            has_b = ins.b is not None
            print(f"{ins.op} {ins.a} {ins.b if has_b else ''}")

    def run(self, halt_on_no_input=False):
        for ins in self.instructions:
            if halt_on_no_input:
                if ins.op == ins._ops["inp"] and not self.registers.inputs:
                    ins_number = self.instructions.index(ins)
                    print(f"halting on instruction {ins_number}")
                    break
            try:
                ins.execute(self.registers)
            except:
                ins_number = self.instructions.index(ins)
                print(f"crashed on instruction {ins_number}")
                raise
