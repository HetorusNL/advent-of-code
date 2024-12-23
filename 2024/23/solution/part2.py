from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.liness = [
            "kh-tc",
            "qp-kh",
            "de-cg",
            "ka-co",
            "yn-aq",
            "qp-ub",
            "cg-tb",
            "vc-aq",
            "tb-ka",
            "wh-tc",
            "yn-cg",
            "kh-ub",
            "ta-co",
            "de-co",
            "tc-td",
            "tb-wq",
            "wh-td",
            "ta-ka",
            "td-qp",
            "aq-cg",
            "wq-ub",
            "ub-vc",
            "de-ta",
            "wq-aq",
            "wq-vc",
            "wh-yn",
            "ka-de",
            "kh-ta",
            "co-tc",
            "wh-qp",
            "tb-vc",
            "td-yn",
        ]

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

    def get_connections(self, computer: str, connections: list[str]):
        group: list[str] = [*connections.copy(), computer]
        num_computers_list: list[int] = []
        for index in group:
            # check how many in the group the index can connect to
            num_computers: int = 0
            for to in group:
                num_computers += to in self.connections[index]
            num_computers_list.append(num_computers)
        # store the number of connections in the group in a 2-level dict
        for i in range(len(group)):
            # for all possible connections in the group, prepare the dict
            if i not in self.num_connections:
                self.num_connections[i] = {}
            # count the number of i-interconnected-computers in this group
            num_i = num_computers_list.count(i)
            if num_i not in self.num_connections[i]:
                self.num_connections[i][num_i] = []
            # add this computer to the calculated number
            self.num_connections[i][num_i].append(computer)

    def find_connection_groups(self):
        self.num_connections: dict[int, dict[int, list[str]]] = {}
        for computer in self.computers:
            self.get_connections(computer, self.connections[computer])

    def parse_results(self):
        # find the highest number of interconnected computers
        for key in sorted(self.num_connections.keys(), reverse=True):
            if key in self.num_connections[key]:
                # we found a pool of the most interconnected computers
                # this must be the answer
                self.result: str = ",".join(sorted(self.num_connections[key][key]))
                return

    def solve(self) -> None:
        print("solving...")
        self.parse_input()
        self.find_connection_groups()
        self.parse_results()

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
