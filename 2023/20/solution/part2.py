from pathlib import Path

from solution.broadcaster import Broadcaster
from solution.conjunction import Conjunction
from solution.flip_flop import FlipFlop
from solution.module import Module


class Part2:
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
        # rx is a conjunction, so all inputs of rx must be True for rx to output False
        output_to_rx = [module.name for module in modules.values() if "rx" in module.outputs]
        inputs_of_rx: dict[str, list[int]] = {
            module.name: [] for module in modules.values() if output_to_rx[0] in module.outputs
        }
        # run the simulation
        iteration = 0
        while iteration := iteration + 1:
            pulses: list[tuple[str, bool, str]] = [("button", False, "broadcaster")]
            idx = 0
            while pulses:
                idx += 1
                new_pulses: list[tuple[str, bool, str]] = []
                for pulse in pulses:
                    pulse_results = modules[pulse[2]].pulse(pulse[0], pulse[1])
                    for module_name, value in pulse_results.items():
                        new_pulses.append((pulse[2], value, module_name))
                pulses = new_pulses
                if iteration > 1:
                    for input_of_rx in inputs_of_rx:
                        input_module: Conjunction = modules[input_of_rx]  # type:ignore
                        if input_module.output_state == True:
                            if iteration not in inputs_of_rx[input_of_rx]:
                                inputs_of_rx[input_of_rx].append(iteration)
            if all(len(input_of_rx) > 1 for input_of_rx in inputs_of_rx.values()):
                self.result = 1
                for input_of_rx in inputs_of_rx.values():
                    self.result *= input_of_rx[-1] - input_of_rx[-2]
                break

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
