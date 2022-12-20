import copy
import re


class Blueprint:
    def __init__(self, blueprint: str):
        # formulate the regex to parse the raw blueprint
        regex = r"Blueprint (?P<id>[0-9]*): "
        regex += r"Each ore robot costs (?P<ore_robot_ore>[0-9]*) ore. "
        regex += r"Each clay robot costs (?P<clay_robot_ore>[0-9]*) ore. "
        regex += r"Each obsidian robot costs (?P<obsidian_robot_ore>[0-9]*) ore "
        regex += r"and (?P<obsidian_robot_clay>[0-9]*) clay. "
        regex += r"Each geode robot costs (?P<geode_robot_ore>[0-9]*) ore "
        regex += r"and (?P<geode_robot_obsidian>[0-9]*) obsidian."
        match = re.match(regex, blueprint)
        assert match, f"invalid blueprint provided: {blueprint}"
        self._id = int(match["id"])
        # store every cost in the class
        self._ore_robot_ore: int = int(match["ore_robot_ore"])
        self._clay_robot_ore: int = int(match["clay_robot_ore"])
        self._obsidian_robot_ore: int = int(match["obsidian_robot_ore"])
        self._obsidian_robot_clay: int = int(match["obsidian_robot_clay"])
        self._geode_robot_ore: int = int(match["geode_robot_ore"])
        self._geode_robot_obsidian: int = int(match["geode_robot_obsidian"])
        # store the robots and inventory in the instances list
        self.INDEX_ORE_ROBOTS = 0
        self.INDEX_CLAY_ROBOTS = 1
        self.INDEX_OBSIDIAN_ROBOTS = 2
        self.INDEX_GEODE_ROBOTS = 3
        self.INDEX_ORE = 4
        self.INDEX_CLAY = 5
        self.INDEX_OBSIDIAN = 6
        self.INDEX_GEODE = 7
        self._instances: list[list[int]] = [
            [
                # store the robots in the instances
                1,  # INDEX_ORE_ROBOTS
                0,  # INDEX_CLAY_ROBOTS
                0,  # INDEX_OBSIDIAN_ROBOTS
                0,  # INDEX_GEODE_ROBOTS
                # store the inventory in the instances
                0,  # INDEX_ORE
                0,  # INDEX_CLAY
                0,  # INDEX_OBSIDIAN
                0,  # INDEX_GEODE
            ]
        ]

    def run_for_minutes(self, minutes: int) -> int:
        cache: dict[str, bool] = {}
        cache_hits: int = 0
        prunes: int = 0
        for minute in range(minutes):
            new_instances: list[list[int]] = []
            for instance in self._instances:
                for new_instance in self._run_minute(instance):
                    hash = self.hash(new_instance)
                    if hash in cache:
                        cache_hits += 1
                    else:
                        cache[hash] = True
                        new_instances.append(new_instance)
            # prune slow versions
            max_geodes = max(instance[self.INDEX_GEODE] for instance in new_instances)
            geode_target = max_geodes // 1
            if geode_target:
                before = len(new_instances)
                new_instances = [instance for instance in new_instances if instance[self.INDEX_GEODE] >= geode_target]
                prunes += before - len(new_instances)
            self._instances = new_instances
            print(
                f"minute: {minute:>01}: new blueprints: {len(self._instances)} "
                f"[cache hits: {cache_hits}, prunes: {prunes}]"
            )
        max_geodes = max(instance[self.INDEX_GEODE] for instance in self._instances)
        self._instances = []  # clear the internal state to reduce memory usage
        return max_geodes

    def _run_minute(self, instance: list[int]) -> list[list[int]]:
        new_instances: list[list[int]] = [instance]
        # try building all robots while this instance does nothing
        if instance[self.INDEX_ORE] >= self._ore_robot_ore:
            new_instance = self._create_copy(instance)
            new_instance[self.INDEX_ORE] -= self._ore_robot_ore
            new_instance[self.INDEX_ORE_ROBOTS] += 1
            new_instances.append(new_instance)
        if instance[self.INDEX_ORE] >= self._clay_robot_ore:
            new_instance = self._create_copy(instance)
            new_instance[self.INDEX_ORE] -= self._clay_robot_ore
            new_instance[self.INDEX_CLAY_ROBOTS] += 1
            new_instances.append(new_instance)
        if (
            instance[self.INDEX_ORE] >= self._obsidian_robot_ore
            and instance[self.INDEX_CLAY] >= self._obsidian_robot_clay
        ):
            new_instance = self._create_copy(instance)
            new_instance[self.INDEX_ORE] -= self._obsidian_robot_ore
            new_instance[self.INDEX_CLAY] -= self._obsidian_robot_clay
            new_instance[self.INDEX_OBSIDIAN_ROBOTS] += 1
            new_instances.append(new_instance)
        if (
            instance[self.INDEX_ORE] >= self._geode_robot_ore
            and instance[self.INDEX_OBSIDIAN] >= self._geode_robot_obsidian
        ):
            new_instance = self._create_copy(instance)
            new_instance[self.INDEX_ORE] -= self._geode_robot_ore
            new_instance[self.INDEX_OBSIDIAN] -= self._geode_robot_obsidian
            new_instance[self.INDEX_GEODE_ROBOTS] += 1
            new_instances.append(new_instance)
        # add resources for the instance blueprint
        self._add_resources(instance)

        return new_instances

    def hash(self, instance: list[int]) -> str:
        return ",".join(map(str, instance))

    def _add_resources(self, instance: list[int]) -> None:
        instance[self.INDEX_ORE] += instance[self.INDEX_ORE_ROBOTS]
        instance[self.INDEX_CLAY] += instance[self.INDEX_CLAY_ROBOTS]
        instance[self.INDEX_OBSIDIAN] += instance[self.INDEX_OBSIDIAN_ROBOTS]
        instance[self.INDEX_GEODE] += instance[self.INDEX_GEODE_ROBOTS]

    def _create_copy(self, instance: list[int]) -> list[int]:
        new_instance: list[int] = [*instance]
        self._add_resources(new_instance)
        return new_instance
