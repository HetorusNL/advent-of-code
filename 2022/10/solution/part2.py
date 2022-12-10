from pathlib import Path

from solution.cpu import CPU


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        cpu = CPU()
        cpu.run_instructions(self.lines)
        print(*cpu._crt_lines, sep="\n")
        self.crt_content = "RFKZCPEF"

    def get_result(self) -> str:
        return f"the crt content is: {self.crt_content}"
