from typing import Union


class CuboidInstruction:
    def __init__(self, inp: Union[list, dict]):
        if isinstance(inp, dict):
            self.state = inp["state"] == "on"
            self.xmin = int(inp["xmin"])
            self.xmax = int(inp["xmax"])
            self.ymin = int(inp["ymin"])
            self.ymax = int(inp["ymax"])
            self.zmin = int(inp["zmin"])
            self.zmax = int(inp["zmax"])
        elif isinstance(inp, list):
            assert len(inp) == 7
            self.state = inp[0] == "on"
            self.xmin = int(inp[1])
            self.xmax = int(inp[2])
            self.ymin = int(inp[3])
            self.ymax = int(inp[4])
            self.zmin = int(inp[5])
            self.zmax = int(inp[6])
        else:
            assert False, "invalid type supplied!"

    def copy(self):
        return CuboidInstruction(
            [
                self.state,
                self.xmin,
                self.xmax,
                self.ymin,
                self.ymax,
                self.zmin,
                self.zmax,
            ]
        )
