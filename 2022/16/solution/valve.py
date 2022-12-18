import re


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
        self._tunnel_names: list[str] = [tunnel.strip() for tunnel in match["tunnels"].split(",")]
        self._tunnels: list["Valve"] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def flow_rate(self) -> int:
        return self._flow_rate

    @property
    def tunnel_names(self) -> list[str]:
        return self._tunnel_names

    @property
    def tunnels(self) -> list["Valve"]:
        return self._tunnels

    def add_tunnel(self, tunnel: "Valve") -> None:
        self._tunnels.append(tunnel)
