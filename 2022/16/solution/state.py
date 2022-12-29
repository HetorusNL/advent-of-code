from solution.valve import Valve


class State:
    def __init__(self, pressure: int, valve: Valve, open_valves: list[Valve]):
        assert len(open_valves) == len(set(open_valves))
        self._pressure: int = pressure
        self._valve: Valve = valve
        self._open_valves: list[Valve] = open_valves

    @property
    def pressure(self) -> int:
        return self._pressure

    @property
    def valve(self) -> Valve:
        return self._valve

    @property
    def open_valves(self) -> list[Valve]:
        return self._open_valves

    @property
    def can_open_valve(self) -> bool:
        valve_not_open = self.valve not in self.open_valves
        has_flow_rate = self.valve.flow_rate > 0
        return valve_not_open and has_flow_rate

    def pressure_after(self, minutes: int):
        flow_rate = sum(valve.flow_rate for valve in self.open_valves)
        return self.pressure + flow_rate * minutes

    def hash(self) -> str:
        # don't add pressure to the hash, as it's used for 2nd tier caching
        return f"[{self.valve.name}, {[valve.name for valve in self.open_valves]}]"

    def __eq__(self, other: "State"):
        return self.pressure == other.pressure and self.valve == other.valve and self.open_valves == other.open_valves

    def __lt__(self, other: "State"):
        return self.pressure < other.pressure

    def __le__(self, other: "State"):
        return self.pressure <= other.pressure
