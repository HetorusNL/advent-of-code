import re


class Part:
    def __init__(self, part: str):
        part_regex = re.compile(r"^x=(?P<x>[0-9]*),m=(?P<m>[0-9]*),a=(?P<a>[0-9]*),s=(?P<s>[0-9]*)$")
        if match := re.match(part_regex, part):
            self.values: dict[str, int] = {}
            self.values["x"] = int(match["x"])
            self.values["m"] = int(match["m"])
            self.values["a"] = int(match["a"])
            self.values["s"] = int(match["s"])
        else:
            assert False

    @property
    def value(self):
        return sum(self.values.values())
