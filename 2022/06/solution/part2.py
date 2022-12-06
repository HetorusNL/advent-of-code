from pathlib import Path

from solution.communication_system import CommunicationSystem


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            lines = [line.strip() for line in f.readlines()]
            assert len(lines) == 1, f"invalid input for this puzzle!"
            self.line = lines[0]

    def solve(self) -> None:
        print("solving...")
        cs = CommunicationSystem()
        cs.add_datastream(self.line)
        self.start_of_message_marker = cs.get_start_of_message_marker()

    def get_result(self) -> str:
        return f"the start of message marker is found at offset: {self.start_of_message_marker}"
