from pathlib import Path

from solution.distress_signal import DistressSignal


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        # add the two divider packets to the lines
        self.lines.extend(["[[2]]", "[[6]]"])
        # add the first packet to the packets list
        packets: list[str] = [self.lines[0]]
        self.lines = self.lines[1:]
        # loop through the lines
        while self.lines:
            line, *self.lines = self.lines
            # discard empty lines
            if not line:
                continue
            # find the correct location for packet (in right order > insert at that index)
            added_packet = False
            for idx, packet in enumerate(packets):
                if DistressSignal(line, packet).is_in_right_order():
                    packets.insert(idx, line)
                    added_packet = True
                    break
            # if the correct location isn't found, the packet must be appended to the back
            if not added_packet:
                packets.append(line)
        # calculate decoder key by multiplying both (indexes + 1)
        self.decoder_key = (packets.index("[[2]]") + 1) * (packets.index("[[6]]") + 1)

    def get_result(self) -> str:
        return f"the decoder key for the distress signal is: {self.decoder_key}"
