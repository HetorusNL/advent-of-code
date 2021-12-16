from packet import Packet


class Solution:
    def __init__(self):
        # some sanity checks
        version_tests = {
            "8A004A801A8002F478": 16,
            "620080001611562C8802118E34": 12,
            "C0015000016115A2E0802F182340": 23,
            "A0016C880162017C3686B18A3D4780": 31,
        }
        for data, version in version_tests.items():
            p_version = Packet(self._parse(data)).parse().recursive_version()
            assert p_version == version

        operator_tests = {
            "C200B40A82": 3,
            "04005AC33890": 54,
            "880086C3E88112": 7,
            "CE00C43D881120": 9,
            "D8005AC2A8F0": 1,
            "F600BC2D8F": 0,
            "9C005AC2F8F0": 0,
            "9C0141080250320F1802104A08": 1,
        }
        for data, value in operator_tests.items():
            assert Packet(self._parse(data)).parse().value == value

        # reset the input for the first part
        self._reset_input()

    def _parse(self, transmission):
        return "".join(bin(int(a, 16))[2:].zfill(4) for a in transmission)

    def _reset_input(self):
        with open("input.txt") as f:
            transmission = f.readline().strip()
        self._raw_packet = self._parse(transmission)

    def solve(self):
        self.part_1()
        self._reset_input()
        self.part_2()

    def part_1(self):
        version = Packet(self._raw_packet).parse().recursive_version()
        print(f"sum of all packets version numbers: {version}")

    def part_2(self):
        value = Packet(self._raw_packet).parse().value
        print(f"value of the hexadecimal-encoded BITS transmission: {value}")


if __name__ == "__main__":
    Solution().solve()
