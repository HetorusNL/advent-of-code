import re

from solution.tunnel import Tunnel


class Valve:
    def __init__(self, line: str):
        # parse the input line
        regex = r"^Valve (?P<name>[A-Z]*) has flow rate=(?P<flow_rate>[0-9]*);"
        regex += r" tunnels? leads? to valves? (?P<tunnels>[A-Z, ]*)$"
        match = re.match(regex, line)
        assert match, f"invalid line provided to valve: {line}"
        # store the values in the class
        self._name: str = match["name"]
        self._flow_rate: int = int(match["flow_rate"])
        self._original_tunnel_names: list[str] = [tunnel.strip() for tunnel in match["tunnels"].split(",")]
        self._tunnels: list[Tunnel] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def flow_rate(self) -> int:
        return self._flow_rate

    @property
    def original_tunnel_names(self) -> list[str]:
        return self._original_tunnel_names

    @property
    def tunnel_names(self) -> list[str]:
        return [tunnel.valve.name for tunnel in self._tunnels]

    @property
    def tunnels(self) -> list[Tunnel]:
        return self._tunnels

    def tunnel(self, name: str) -> Tunnel:
        tunnels = [tunnel for tunnel in self.tunnels if tunnel.valve.name == name]
        assert len(tunnels) == 1
        return tunnels[0]

    def add_tunnel(self, tunnel: Tunnel) -> None:
        self._tunnels.append(tunnel)

    def remove_tunnel(self, valve_name: str) -> None:
        self._tunnels = [tunnel for tunnel in self._tunnels if tunnel.valve.name != valve_name]

    def __lt__(self, other: "Valve"):
        return self.name < other.name
