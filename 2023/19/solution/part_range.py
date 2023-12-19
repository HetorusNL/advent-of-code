class PartRange:
    def __init__(self):
        self.values: dict[str, dict[str, int]] = {
            "x": {"min": 1, "max": 4000},
            "m": {"min": 1, "max": 4000},
            "a": {"min": 1, "max": 4000},
            "s": {"min": 1, "max": 4000},
        }

    def solvable(self) -> bool:
        for entry in self.values.values():
            if entry["min"] > entry["max"]:
                return False
        return True

    @property
    def result(self) -> int:
        _result = 1
        for entry in self.values.values():
            _result *= entry["max"] - entry["min"] + 1
        return _result
