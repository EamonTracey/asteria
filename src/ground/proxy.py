from dataclasses import dataclass
import logging
import socket
import traceback

import adafruit_rfm9x

from base.component import Component

logger = logging.getLogger(__name__)

MAX_MESSAGES = 10


@dataclass
class ProxyState:
    ...


class ProxyComponent(Component):

    def __init__(self, host: tuple[str, int], port: int,
                 rfm95w: adafruit_rfm9x.RFM9x):
        self._state = ProxyState()

        self._host = host
        self._rfm95w = rfm95w

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(("0.0.0.0", port))
        self._socket.setblocking(False)

        logger.info(f"Initialized proxy between host and air.")
        logger.info(f"{port=}")
        logger.info(f"{host=}")

    @property
    def state(self):
        return self._state

    def dispatch(self):
        for _ in range(MAX_MESSAGES):
            # Receive data from the host machine to be sent to the air.
            try:
                message, _ = self._socket.recvfrom(4096)
                self._proxy_to_air(message)
            except BlockingIOError:
                break

        # Send data received from the air to the host machine.
        for _ in range(MAX_MESSAGES):
            message = self._rfm95w.receive(timeout=0)
            if message is None:
                break
            self._proxy_to_host(bytes(message))

    def _proxy_to_air(self, message: bytes):
        success = self._rfm95w.send(message)
        if not success:
            logger.error(
                f"Failed to proxy {message=} to air: {traceback.format_exc()}")

    def _proxy_to_host(self, message: bytes):
        try:
            self._socket.sendto(message, self._host)
        except BlockingIOError:
            logger.error(
                f"Failed to proxy {message=} to host: {traceback.format_exc()}"
            )
