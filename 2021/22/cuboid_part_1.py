from cuboid_instruction import CuboidInstruction
from typing import Dict


class CuboidPart1:
    def __init__(self):
        # cuboid [x] [y] [z]
        self.cuboid: Dict[int, Dict[int, Dict[int, bool]]] = {}

    def perform_instruction(self, instruction: CuboidInstruction):
        if self._should_ignore(instruction):
            return
        for x in range(instruction.xmin, instruction.xmax + 1):
            if x not in self.cuboid:
                self.cuboid[x] = {}
            for y in range(instruction.ymin, instruction.ymax + 1):
                if y not in self.cuboid[x]:
                    self.cuboid[x][y] = {}
                for z in range(instruction.zmin, instruction.zmax + 1):
                    self.cuboid[x][y][z] = instruction.state

    def on_cubes(self):
        cubes = 0
        for x_key, x_val in self.cuboid.items():
            for y_key, y_val in x_val.items():
                for z_key, z_val in y_val.items():
                    cubes += int(z_val)
        return cubes

    def _should_ignore(self, ci: CuboidInstruction):
        for val in [ci.xmin, ci.xmax, ci.ymin, ci.ymax, ci.zmin, ci.zmax]:
            if val < -50 or val > 50:
                return True
        return False
