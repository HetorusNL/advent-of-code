class Packet:
    def __init__(self, _raw_packet):
        self._raw_packet = _raw_packet
        self.version = None
        self.type = None
        self.length = None
        self.value = None
        self.operator = None
        self.length_type_id = None
        self.sub_packets = []

        self._type_parser = {
            0: self._operator_parser,
            1: self._operator_parser,
            2: self._operator_parser,
            3: self._operator_parser,
            4: self._literal_parser,
            5: self._operator_parser,
            6: self._operator_parser,
            7: self._operator_parser,
        }
        self._operators = {
            0: self._sum,
            1: self._product,
            2: self._minimum,
            3: self._maximum,
            5: self._greater_than,
            6: self._less_than,
            7: self._equal_to,
        }

    def parse(self):
        self.version = int(self._raw_packet[0:3], 2)
        self.type = int(self._raw_packet[3:6], 2)
        # parse the type specific portion of the packet
        self._type_parser.get(self.type, self._operator_parser)()
        return self

    def recursive_version(self):
        version = self.version
        for sub_packet in self.sub_packets:
            version += sub_packet.recursive_version()
        return version

    def _literal_parser(self):
        index = 6
        value = ""
        while True:
            chunk = self._raw_packet[index : index + 5]
            value += chunk[1:]
            index += 5
            if chunk[0] == "0" or index > len(self._raw_packet):
                break
        self.value = int(value, 2)
        self.length = index

    def _operator_parser(self):
        self.operator = self._operators[self.type]
        self.length_type_id = int(self._raw_packet[6])
        if self.length_type_id == 0:
            # process for this total length in bits
            subpackets_length = int(self._raw_packet[7:22], 2)
            total_length = 0
            while total_length < subpackets_length:
                total_length += self._parse_sub_packet(22 + total_length)
            self.length = 22 + total_length
        else:  # length_type_id == 1
            # process this amount of packets
            num_packets = int(self._raw_packet[7:18], 2)
            total_length = 0
            for _ in range(num_packets):
                total_length += self._parse_sub_packet(18 + total_length)
            self.length = 18 + total_length
        self.operator()

    def _parse_sub_packet(self, offset):
        new_packet = Packet(self._raw_packet[offset:]).parse()
        self.sub_packets.append(new_packet)
        return new_packet.length

    # operator functions

    def _sum(self):
        self.value = sum(packet.value for packet in self.sub_packets)

    def _product(self):
        value = 1
        for packet in self.sub_packets:
            value *= packet.value
        self.value = value

    def _minimum(self):
        self.value = min(packet.value for packet in self.sub_packets)

    def _maximum(self):
        self.value = max(packet.value for packet in self.sub_packets)

    def _greater_than(self):
        self.value = int(self.sub_packets[0].value > self.sub_packets[1].value)

    def _less_than(self):
        self.value = int(self.sub_packets[0].value < self.sub_packets[1].value)

    def _equal_to(self):
        self.value = int(
            self.sub_packets[0].value == self.sub_packets[1].value
        )
