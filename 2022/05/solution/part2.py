from pathlib import Path
import re

from solution.stack import Stack


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.removesuffix("\n") for line in f.readlines()]
        # the global stack object to store the crates
        self.stack: Stack = Stack()
        for line_idx, line in enumerate(self.lines):
            if re.match(r"^[0-9 ]*$", line):
                self.lines = self.lines[line_idx + 2 :]
                break
            idx = 0
            while line:
                idx += 1  # we use indexing by 1 in this puzzle
                # extract the line section with a single crate from the line
                section, line = line[:3], line[4:]
                if match := re.match(r"\[(?P<letter>[A-Z])\]", section):
                    self.stack.push_back(str(idx), match["letter"])
        # reverse the stack as we populated it in reverse order
        self.stack.reverse_stack()

    def solve(self) -> None:
        print("solving...")
        regex = re.compile(r"^move (?P<num>[0-9]*) from (?P<from>[0-9]*) to (?P<to>[0-9]*)$")
        for line in self.lines:
            match = re.match(regex, line)
            assert match
            move = self.stack.pop_multiple(match["from"], int(match["num"]))
            self.stack.push_back_multiple(match["to"], move)

    def get_result(self) -> str:
        result = ""
        for idx in range(1, self.stack.num_stacks() + 1):
            result += self.stack.pop(str(idx))
        return f"the crates on top of the stacks after CrateMover 9001 rearrangement are: {result}"
