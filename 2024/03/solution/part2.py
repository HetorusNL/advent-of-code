from pathlib import Path
import re


class Result:
    def __init__(self, offset: int, func: str, value: int | None = None):
        self.offset: int = offset
        self.func: str = func
        self.value: int | None = value


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        enabled = True
        for line in self.lines:
            offset = 0
            while True:
                results: list[Result] = []

                # regex search for mul, add to results if found
                if match := re.search(r"mul\((?P<left>[0-9]*),(?P<right>[0-9]*)\)", line[offset:]):
                    value = int(match.groupdict()["left"]) * int(match.groupdict()["right"])
                    results.append(Result(match.end(), "mul", value))
                # regex search for don't, add to results if found
                if match := re.search(r"don't\(\)", line[offset:]):
                    results.append(Result(match.end(), "dont"))
                # regex search for do, add to results if found
                if match := re.search(r"do\(\)", line[offset:]):
                    results.append(Result(match.end(), "do"))

                # if we have results, process the one with the lowest offset
                if results:
                    result = sorted(results, key=lambda r: r.offset)[0]
                    offset += result.offset
                    match result.func:
                        case "mul":
                            assert result.value
                            if enabled:
                                self.result += result.value
                        case "dont":
                            enabled = False
                        case "do":
                            enabled = True
                        case _:
                            assert False
                # otherwise, when no results, break from the loop
                else:
                    break

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
