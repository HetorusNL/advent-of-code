class Submarine2:
    def __init__(self):
        self._instruction_set = {
            "forward": self._forward,
            "up": self._up,
            "down": self._down,
        }
        self._horizontal_pos = 0
        self._depth = 0
        self._aim = 0

    def run_program(self, raw_instructions):
        for raw_instruction in raw_instructions:
            instruction = self._parse_instruction(raw_instruction)
            self._instruction_set[instruction["direction"]](instruction)

    def final_value(self):
        return self._horizontal_pos * self._depth

    def _parse_instruction(self, raw_instruction):
        data = raw_instruction.split()
        return {"direction": data[0], "speed": int(data[1])}

    def _forward(self, instruction):
        self._horizontal_pos += instruction["speed"]
        self._depth += self._aim * instruction["speed"]

    def _up(self, instruction):
        self._aim -= instruction["speed"]

    def _down(self, instruction):
        self._aim += instruction["speed"]
