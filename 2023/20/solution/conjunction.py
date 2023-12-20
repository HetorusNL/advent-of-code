from solution.module import Module


class Conjunction(Module):
    def __init__(self, name: str, results: dict[bool, int]):
        Module.__init__(self, name, results)
        self.output_state = True

    def prepare(self):
        Module.prepare(self)
        self.input_state: dict[str, bool] = {}
        for _input in self.inputs:
            self.input_state[_input] = False

    def pulse(self, pulse_from: str, value: bool) -> dict[str, bool]:
        Module.pulse(self, pulse_from, value)
        self.input_state[pulse_from] = value
        result: dict[str, bool] = {}
        if all(value == True for value in self.input_state.values()):
            for output in self.outputs:
                result[output] = False
                self.output_state = False
        else:
            for output in self.outputs:
                result[output] = True
                self.output_state = True
        return result
