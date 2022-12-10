from solution.instruction import Instruction


class CPU:
    def __init__(self):
        self._instructions: list[Instruction] = []
        self._registers: dict[str, int] = {"x": 1}
        self._cycle_counter = 0
        self._cycle_counter_target = 20
        self._signal_strength = 0
        self._crt_lines: list[str] = []

    @property
    def signal_strength(self):
        return self._signal_strength

    def run_instructions(self, lines):
        # add and run all instructions
        while lines:
            if not self._instructions:
                line, *lines = lines
                self._instructions.append(Instruction(line))
            self._run_instructions()

        # while instructions remain, keep running them
        while self._instructions:
            self._run_instructions()

    def _run_instructions(self):
        # increment the cycle counter
        self._cycle_counter += 1
        # if cycle counter in [20, 60, 100, 140, 180, ..]
        if self._cycle_counter == self._cycle_counter_target:
            # add to signal strength: cycle_counter * register X
            self._cycle_counter_target += 40
            self._signal_strength += self._cycle_counter * self._registers["x"]

        # pos is 0-based
        pos = (self._cycle_counter - 1) % 40
        # every time pos is 0, add a new (empty) line to the crt
        if pos == 0:
            self._crt_lines.append("")
        # add '#' if register X is within 1 position around pos else '.'
        if self._registers["x"] - 1 <= pos and self._registers["x"] + 1 >= pos:
            self._crt_lines[-1] += "#"
        else:
            self._crt_lines[-1] += "."

        # process all instructions (if present)
        instr_number = 0
        while instr_number < len(self._instructions):
            instruction = self._instructions[instr_number]
            instruction.run(self._registers)
            if instruction.is_complete:
                self._instructions.remove(instruction)
            else:
                instr_number += 1
