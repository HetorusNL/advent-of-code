from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from solution.valve import Valve


class Tunnel:
    def __init__(self, valves_in_tunnel: list[str], valve: Valve):
        self._valves_in_tunnel: list[str] = list(set(valves_in_tunnel))
        self._length: int = len(self.valves_in_tunnel) - 1
        self._valve: Valve = valve

    @property
    def valves_in_tunnel(self) -> list[str]:
        return self._valves_in_tunnel

    @property
    def length(self) -> int:
        return self._length

    @property
    def valve(self) -> Valve:
        return self._valve
