class Cave:
    def __init__(self, name: str):
        self.name = name
        self.big = name.upper() == name
        self.adjacent_caves = []

    def resolve(self, cave_names, caves):
        for cave_name in cave_names:
            if self.name == cave_name[0]:
                for cave in caves:
                    if cave.name == cave_name[1]:
                        self.adjacent_caves.append(cave)
            if self.name == cave_name[1]:
                for cave in caves:
                    if cave.name == cave_name[0]:
                        self.adjacent_caves.append(cave)
        return self

    def can_visit1(self, cave, path):
        return not cave in path or cave.big

    def can_visit2(self, cave, path):
        can_visit_small_cave = self.can_visit_small_cave(path, cave)
        return not cave in path or cave.big or can_visit_small_cave

    def can_visit_small_cave(self, path, cave):
        small_caves = []
        if cave.name == "start":
            return False
        for cave in path:
            if not cave.big and cave.name in small_caves:
                return False
            small_caves.append(cave.name)
        return True

    def __eq__(self, other):
        """implements 'Cave(..) in [..]' (Cave in list) functionality"""
        return self.name == other.name
