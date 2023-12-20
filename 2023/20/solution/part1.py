from pathlib import Path

from solution.broadcaster import Broadcaster
from solution.conjunction import Conjunction
from solution.flip_flop import FlipFlop
from solution.module import Module


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.result = 42
        results: dict[bool, int] = {True: 0, False: 0}
        modules: dict[str, Module] = {}
        # create the modules
        for line in self.lines:
            _input = line.split(" -> ")[0]
            if _input[0] == "%":
                modules[_input[1:]] = FlipFlop(_input[1:], results)
            elif _input[0] == "&":
                modules[_input[1:]] = Conjunction(_input[1:], results)
            elif _input == "broadcaster":
                modules[_input] = Broadcaster(_input, results)
            else:
                assert False
        # link the modules
        for line in self.lines:
            _input, outputs = line.split(" -> ")
            _input = _input.replace("%", "")
            _input = _input.replace("&", "")
            for output in outputs.split(", "):
                modules[_input].outputs.append(output)
                if output not in modules:
                    modules[output] = Module(output, results)
                modules[output].inputs.append(_input)
        # prepare the modules
        for module in modules.values():
            module.prepare()
        # run the simulation
        iterations = 1000
        for _ in range(1, iterations + 1):
            pulses: list[tuple[str, bool, str]] = [("button", False, "broadcaster")]
            while pulses:
                new_pulses: list[tuple[str, bool, str]] = []
                for pulse in pulses:
                    pulse_results = modules[pulse[2]].pulse(pulse[0], pulse[1])
                    for module_name, value in pulse_results.items():
                        new_pulses.append((pulse[2], value, module_name))
                pulses = new_pulses
        self.result = results[True] * results[False]

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
