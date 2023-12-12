from pathlib import Path
import time


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.lines = [
            "???.### 1,1,3",
            ".??..??...?##. 1,1,3",
            "?#?#?#?#?#?#?#? 1,3,1,6",
            "????.#...#... 4,1,1",
            "????.######..#####. 1,6,5",
            "?###???????? 3,2,1",
        ]
        ".#.###.#?#?#?#? 1,3,1,6",

    def solve(self) -> None:
        print("solving...")
        for line in self.lines:
            self.result = 0
            self.cache = {}
            print(f"parsing {line}")
            self.parse_line(line)

            print(self.result)
            print(self.cache)
            input()
        exit(0)

    def parse_line(self, line: str):
        springs, values_str = line.split(" ")
        values = list(map(int, values_str.split(",")))
        # unfold the paper
        # springs = "?".join([springs] * 5)
        # values = values * 5

        print(springs, values)
        self.fill_first(springs.strip("."), values)

    def fill_first(self, springs, values, result=""):
        # time.sleep(0.25)
        print(springs, values)

        if not springs:
            if not values:  # if there are values left, we have failed
                # on an empty string, we have completed the line
                self.result += 1
                self.cache[result] = True
                print("success!")
            print("return no springs")
            return

        if not values:
            if "#" not in springs:
                # success
                self.result += 1
                self.cache[result] = True
                print("success!")
                return

        if len(springs) == values[0]:
            if springs.count("#") == values[0]:
                # success
                self.result += 1
                self.cache[result] = True
                print("success!")
                return

        if len(springs) < sum(values) + len(values) - 1:
            # not enough characters to fill the values
            print("return, no springs left")
            return

        if springs and not values:
            # springs left, but no values to fill: fail
            print("return springs and no values")
            return

        # prune first value if available
        if springs.startswith("#" * values[0]):
            if springs[values[0]] == "#":
                print("return illegal start")
                return
            result += "#" * values[0]
            new_springs = springs[values[0] + 1 :]
            springs = new_springs.strip(".")
            result += "." * (len(springs) - len(new_springs))
            values = values[1:]

        # fill with good
        new_springs = springs.replace("?", ".", 1).strip(".")
        self.fill_first(new_springs, values, result + "." * (len(springs) - len(new_springs)))

        # fill with broken
        print(values, springs)
        group = springs[: values[0]]
        if "." in group:
            # we can't make a group here, this line fails
            print("return . in group")
            return
        print("pruned")
        # recurse if we have springs left
        new_springs = springs[values[0] + 1 :].strip(".")
        value0 = values[0]
        self.fill_first(
            new_springs, values[1:], result + "#" * value0 + "." * (len(springs) - len(new_springs) - value0)
        )

    def replace_attempt(self, springs: str, attempt) -> str:
        attempt = attempt.replace("1", "#")
        attempt = attempt.replace("0", ".")
        for char in attempt:
            springs = springs.replace("?", char, 1)
        return springs

    def spring_correct(self, values: list[int], parse_line: str):
        spring_groups = list(map(len, filter(lambda a: a, parse_line.split("."))))
        return spring_groups == values

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
