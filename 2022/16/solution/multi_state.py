from solution.valve import Valve


class MultiState:
    def __init__(self, pressure: int, valves: tuple[Valve, Valve], open_valves: list[Valve], flow_rate: int):
        # open_valves_list = [valve.name for valve in open_valves]
        # open_valves_set = [valve.name for valve in set(open_valves)]
        # assert len(open_valves) == len(set(open_valves)), f"{open_valves_list} != {open_valves_set}!"
        self._pressure: int = pressure
        self._valves: tuple[Valve, Valve] = tuple(sorted(valves))
        self._open_valves: list[Valve] = open_valves
        self._flow_rate: int = flow_rate

    @property
    def pressure(self) -> int:
        return self._pressure

    @property
    def valves(self) -> tuple[Valve, Valve]:
        return self._valves

    @property
    def open_valves(self) -> list[Valve]:
        return self._open_valves

    @property
    def flow_rate(self) -> int:
        return self._flow_rate

    def can_open_valve(self, index: int) -> bool:
        valve_not_open = self.valves[index] not in self.open_valves
        has_flow_rate = self.valves[index].flow_rate > 0
        return valve_not_open and has_flow_rate

    def pressure_after(self, minutes: int):
        return self.pressure + self._flow_rate * minutes

    def hash(self) -> str:
        # don't add pressure to the hash, as it's used for 2nd tier caching
        valves = f"[{self.valves[0].name}, {self.valves[1].name}]"
        return f"[{valves}, {[valve.name for valve in self.open_valves]}]"

    def __eq__(self, other: "MultiState"):
        return (
            self.pressure == other.pressure and self.valves == other.valves and self.open_valves == other.open_valves
        )

    def __lt__(self, other: "MultiState"):
        return self.pressure < other.pressure

    def __le__(self, other: "MultiState"):
        return self.pressure <= other.pressure
