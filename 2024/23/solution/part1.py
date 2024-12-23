from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def add_connection(self, left: str, right: str):
        if left not in self.connections:
            self.connections[left] = []
        assert right not in self.connections[left]
        self.connections[left].append(right)

    def parse_input(self):
        self.connections: dict[str, list[str]] = {}
        for line in self.lines:
            left, right = [side.strip() for side in line.split("-")]
            # add the connection both ways
            self.add_connection(left, right)
            self.add_connection(right, left)
        # create the set of unique computers in the graph
        self.computers: set[str] = set(self.connections.keys())

    def single_connect(self, first_computer: str, computers: list[str]):
        # check if we have found our loop of 3
        if len(computers) == 3 + 1:
            if computers[-1] == first_computer:
                # check that at least 1 computer starts with a "t"
                if any(c.startswith("t") for c in computers):
                    group: str = ",".join(sorted(computers[1:]))
                    if group not in self.groups:
                        self.groups.append(group)
            return
        # recurse into all connections
        for computer in self.connections[computers[-1]]:
            new_computers = computers.copy()
            new_computers.append(computer)
            self.single_connect(first_computer, new_computers)

    def find_groups(self):
        self.groups: list[str] = []
        for computer in self.computers:
            self.single_connect(computer, [computer])

    def solve(self) -> None:
        print("solving...")
        self.parse_input()
        self.find_groups()
        self.result: int = len(self.groups)

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
