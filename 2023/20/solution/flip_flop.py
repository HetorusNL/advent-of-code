from solution.module import Module


class FlipFlop(Module):
    def __init__(self, name: str, results: dict[bool, int]):
        Module.__init__(self, name, results)

    def prepare(self):
        Module.prepare(self)
        self.state = False

    def pulse(self, pulse_from: str, value: bool) -> dict[str, bool]:
        Module.pulse(self, pulse_from, value)
        result: dict[str, bool] = {}
        if value == False:
            self.state = not self.state
            for output in self.outputs:
                result[output] = self.state
        return result
