from dataclasses import dataclass
import socket
from typing import Optional

from base.component import Component


@dataclass
class CommandState:
    command: Optional[int] = None


class CommandComponent(Component):

    def __init__(self, port: int):
        self._state = CommandState()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(("0.0.0.0", port))
        self._socket.setblocking(False)

    @property
    def state(self):
        return self._state

    def dispatch(self):
        try:
            command, _ = self._socket.recvfrom(4096)
        except BlockingIOError:
            return

        command = int.from_bytes(command, byteorder="big")
        self._state.command = command
