from cuboid_instruction import CuboidInstruction


class CuboidPart2:
    def __init__(self, instruction: CuboidInstruction):
        self._instr: CuboidInstruction = instruction
        self._off_cuboids = []  # CuboidPart2 list with nested intersections
        self._volume = (
            (self._instr.xmax + 1 - self._instr.xmin)
            * (self._instr.ymax + 1 - self._instr.ymin)
            * (self._instr.zmax + 1 - self._instr.zmin)
        )

    def intersect(self, intersect_instr: CuboidInstruction):
        ins = self._instr.copy()
        ins.xmin = max(self._instr.xmin, intersect_instr.xmin)
        ins.xmax = min(self._instr.xmax, intersect_instr.xmax)
        ins.ymin = max(self._instr.ymin, intersect_instr.ymin)
        ins.ymax = min(self._instr.ymax, intersect_instr.ymax)
        ins.zmin = max(self._instr.zmin, intersect_instr.zmin)
        ins.zmax = min(self._instr.zmax, intersect_instr.zmax)
        # return if not intersecting
        if ins.xmax < ins.xmin or ins.ymax < ins.ymin or ins.zmax < ins.zmin:
            return
        # apply intersection function to all current off_cuboids
        for off_cuboid in self._off_cuboids:
            off_cuboid.intersect(ins)
        # add this new intersect cuboid to the cuboid list
        self._off_cuboids.append(CuboidPart2(ins))

    def on_cubes(self):
        return self._volume - sum(cub.on_cubes() for cub in self._off_cuboids)
