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
        # store the robots in the class
        self._ore_robots: int = 1
        self._clay_robots: int = 0
        self._obsidian_robots: int = 0
        self._geode_robots: int = 0
        # store the inventory in the class
        self._ore: int = 0
        self._clay: int = 0
        self._obsidian: int = 0
        self._geode: int = 0

    def run_minute(self) -> list["Blueprint"]:
        blueprints: list["Blueprint"] = [self]
        # try building all robots while this instance does nothing
        if self._ore >= self._ore_robot_ore:
            new_blueprint = self._create_copy()
            new_blueprint._ore -= self._ore_robot_ore
            new_blueprint._ore_robots += 1
            blueprints.append(new_blueprint)
        if self._ore >= self._clay_robot_ore:
            new_blueprint = self._create_copy()
            new_blueprint._ore -= self._clay_robot_ore
            new_blueprint._clay_robots += 1
            blueprints.append(new_blueprint)
        if self._ore >= self._obsidian_robot_ore and self._clay >= self._obsidian_robot_clay:
            new_blueprint = self._create_copy()
            new_blueprint._ore -= self._obsidian_robot_ore
            new_blueprint._clay -= self._obsidian_robot_clay
            new_blueprint._obsidian_robots += 1
            blueprints.append(new_blueprint)
        if self._ore >= self._geode_robot_ore and self._obsidian >= self._geode_robot_obsidian:
            new_blueprint = self._create_copy()
            new_blueprint._ore -= self._geode_robot_ore
            new_blueprint._obsidian -= self._geode_robot_obsidian
            new_blueprint._geode_robots += 1
            blueprints.append(new_blueprint)
        # add resources for the self blueprint
        self._add_resources()

        return blueprints

    def hash(self) -> str:
        return ",".join(
            map(
                str,
                [
                    self._ore_robots,
                    self._clay_robots,
                    self._obsidian_robots,
                    self._geode_robots,
                    self._ore,
                    self._clay,
                    self._obsidian,
                    self._geode,
                ],
            )
        )

    def sum_robots(self) -> int:
        return self._ore_robots + self._clay_robots + self._obsidian_robots + self._geode_robots

    def _add_resources(self) -> None:
        self._ore += self._ore_robots
        self._clay += self._clay_robots
        self._obsidian += self._obsidian_robots
        self._geode += self._geode_robots

    def _create_copy(self) -> "Blueprint":
        _copy = type(self).__new__(type(self))
        _copy.__dict__.update(self.__dict__)
        _copy._add_resources()
        return _copy
