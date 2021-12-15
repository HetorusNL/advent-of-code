from node import Node
from typing import Dict, List


class Solution:
    def __init__(self):
        self._reset_input()

    def _reset_input(self, full_map=False):
        # the risk level map
        self._rlm: Dict[int, Dict[int, int]] = {}
        self._nodes: Dict[int, Dict[int, Node]] = {}
        self.viewed_nodes_list: List[Node] = []

        with open("input.txt") as f:
            lines = [line.strip() for line in f.readlines()]

        w = len(lines[0])
        h = len(lines)

        if full_map:
            for x in range(w * 5):
                self._rlm[x] = {}
                self._nodes[x] = {}
                for y in range(h * 5):
                    risk = int(lines[y % h][x % w]) + x // w + y // h
                    self._rlm[x][y] = (risk - 1) % 9 + 1
                    self._nodes[x][y] = Node(x, y, w * 5, h * 5, self._nodes)
            self.w = w * 5
            self.h = h * 5
        else:
            for x in range(w):
                self._rlm[x] = {}
                self._nodes[x] = {}
                for y in range(h):
                    self._rlm[x][y] = int(lines[y][x])
                    self._nodes[x][y] = Node(x, y, w, h, self._nodes)
            self.w = w
            self.h = h

    def solve(self):
        self.part_1()
        self._reset_input(full_map=True)
        self.part_2()

    def part_1(self):
        self._do_dijkstra()
        risk = self._nodes[self.w - 1][self.h - 1].distance
        print("with original map: ", end="")
        print(f"lowest total risk from top left to bottom right: {risk}")

    def part_2(self):
        self._do_dijkstra()
        risk = self._nodes[self.w - 1][self.h - 1].distance
        print("with the full map: ", end="")
        print(f"lowest total risk from top left to bottom right: {risk}")

    def _do_dijkstra(self):
        node = self._nodes[0][0]
        node.distance = 0
        self.viewed_nodes_list = []
        while True:
            # loop through the adjacent nodes and update the tentative distance
            for adjacent_node in node.adjacent_nodes_hv():
                if not adjacent_node.visited:
                    # distance value (risk) of the target point
                    distance = self._rlm[adjacent_node.x][adjacent_node.y]
                    # calculate tentative distance
                    new_tentative_distance = node.distance + distance
                    # if tentative distance is lower, update node distance
                    adjacent_node.distance = min(
                        adjacent_node.distance, new_tentative_distance
                    )
                    if adjacent_node not in self.viewed_nodes_list:
                        self.viewed_nodes_list.append(adjacent_node)
            node.visited = True
            if node in self.viewed_nodes_list:
                self.viewed_nodes_list.remove(node)
            # if the end node is visited, the algorithm is finished
            if self._nodes[self.w - 1][self.h - 1].visited:
                break
            # select a new unvisited node with the lowest tentative distance
            node = self._select_next_node()
            # if not Node (all distances infinite) no path could be planned
            assert Node is not None
            # self._print_nodes()  # print the visisted nodes
            # self._print_path()  # print the planned path (distances)
            # time.sleep(0.1)  # to be able to see the updates
        # self._print_path()  # print the path after the algorithm is finished

    def _select_next_node(self) -> Node:
        distance = float("inf")
        node = None
        for n in self.viewed_nodes_list:
            if n.distance < distance:
                distance = n.distance
                node = n
        return node

    def _print_nodes(self):
        visited = lambda x, y: "X" if self._nodes[x][y].visited else "-"
        for y in range(self.h):
            print("".join(visited(x, y) for x in range(self.w)))

    def _print_path(self):
        _max = 0
        for y in range(self.h):
            for x in range(self.w):
                _max = max(_max, self._nodes[x][y].distance)

        for y in range(self.h):
            for x in range(self.w):
                distance = self._nodes[x][y].distance
                print(f"{distance}".rjust(len(str(_max)) + 1), end="")
            print()


if __name__ == "__main__":
    Solution().solve()
