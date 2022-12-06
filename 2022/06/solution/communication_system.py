from solution.queue import Queue


class CommunicationSystem:
    def __init__(self):
        self._datastream: str = ""

    def add_datastream(self, datastream: str):
        self._datastream: str = datastream

    def get_start_of_packet_marker(self) -> int:
        return self._get_start_marker(distinct_characters=4)

    def get_start_of_message_marker(self) -> int:
        return self._get_start_marker(distinct_characters=14)

    def _get_start_marker(self, distinct_characters: int) -> int:
        queue = Queue(size=distinct_characters)
        while self._datastream:
            char, *self._datastream = self._datastream
            queue.push_back(char)
            if queue.header_found():
                return queue.header_offset()
        return -1
