class Module:
    def __init__(self, name: str, results: dict[bool, int]):
        self.name = name
        self.results = results
        self.inputs: list[str] = []
        self.outputs: list[str] = []

    def prepare(self):
        pass

    def pulse(self, pulse_from: str, value: bool) -> dict[str, bool]:
        self.results[value] += 1
        return {}
