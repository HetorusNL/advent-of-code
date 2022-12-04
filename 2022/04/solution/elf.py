class Elf:
    def __init__(self, start: int, end: int):
        self.start: int = start
        self.end: int = end

    @classmethod
    def parse_elf_line(cls, line: str) -> tuple["Elf", "Elf"]:
        raw_elf1, raw_elf2 = line.split(",")
        elf1 = Elf(*[int(num) for num in raw_elf1.split("-")])
        elf2 = Elf(*[int(num) for num in raw_elf2.split("-")])
        return elf1, elf2

    def fully_contains(self, other: "Elf"):
        # check if other elf fits in self
        if self.start <= other.start and self.end >= other.end:
            return True
        # check if self fits in other elf
        if other.start <= self.start and other.end >= self.end:
            return True
        # both are not true, so no elf fully contains the other
        return False

    def overlaps(self, other: "Elf"):
        # check if self starts somewhere in other elf
        if self.start >= other.start and self.start <= other.end:
            return True
        # check if other elf starts somewhere in self
        if other.start >= self.start and other.start <= self.end:
            return True
        # both are not true, so there is no overlap between the elves
        return False
