from pair import Pair


class Solution:
    def __init__(self):
        self._reset_input()

    def _reset_input(self):
        polymer_template = []
        self._pairs = {}
        self._last_pair = None
        with open("input.txt") as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if " -> " in line:
                pair, result = line.split(" -> ")
                self._pairs[pair] = Pair(pair, result)
            elif len(line) > 0:
                polymer_template = line
        for i in range(len(polymer_template) - 1):
            self._pairs[polymer_template[i : i + 2]].counter += 1
            self._last_pair = self._pairs[polymer_template[i : i + 2]]

    def solve(self):
        self.part_1()
        self._reset_input()
        self.part_2()

    def part_1(self):
        self._run_steps(10)

    def part_2(self):
        self._run_steps(40)

    def _run_steps(self, num):
        for _ in range(num):
            self._pair_insertion()
        element_count = self._extract_elements()
        most = max(element_count, key=element_count.get)
        least = min(element_count, key=element_count.get)
        result = element_count[most] - element_count[least]
        print(f"{num} steps: ", end="")
        print(f"num most common element - num least common element: {result}")

    def _pair_insertion(self):
        step_results = []
        # apply the step to each pair
        for _, p in self._pairs.items():
            step_results.append(p.step())
        # reset the counters
        for _, p in self._pairs.items():
            p.counter = 0
        # add the resulting pairs from the pair steps (2 new pair per pair)
        for step_result in step_results:
            for k, v in step_result.items():
                self._pairs[k].add(v)

    def _extract_elements(self):
        # individual element result
        elements = {}
        # loop through the pairs
        for k, v in self._pairs.items():
            # if the pair exist (has a counter value)
            if v.counter:
                # add the couunter of the first element of the pair to elements
                if k[0] not in elements:
                    elements[k[0]] = 0
                elements[k[0]] += v.counter
        # add 1 to the last element of the last pair
        if self._last_pair.counter:
            if self._last_pair.pair[1] not in elements:
                elements[self._last_pair.pair[1]] = 0
            elements[self._last_pair.pair[1]] += 1
        return elements


if __name__ == "__main__":
    Solution().solve()
