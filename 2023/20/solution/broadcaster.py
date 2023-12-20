from solution.module import Module


class Broadcaster(Module):
    def __init__(self, name: str, results: dict[bool, int]):
        Module.__init__(self, name, results)

    def prepare(self):
        Module.prepare(self)

    def pulse(self, pulse_from: str, value: bool) -> dict[str, bool]:
        Module.pulse(self, pulse_from, value)
        result: dict[str, bool] = {}
        for output in self.outputs:
            result[output] = value
        return result
