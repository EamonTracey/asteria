from dataclasses import dataclass
from typing import Optional

import adafruit_rfm9x
import busio
import digitalio
import microcontroller

from air.bno085 import BNO085State
from air.lidar import LidarState
from base.component import Component

MAX_MESSAGES = 10


@dataclass
class RFM95WState:
    command: Optional[int] = None


class RFM95WComponent(Component):

    def __init__(self, spi: busio.SPI, cs: microcontroller.Pin,
                 rst: microcontroller.Pin, bno085_state: BNO085State,
                 lidar_state, LidarState):
        self._state = RFM95WState()

        self._bno085_state = bno085_state
        self._lidar_state = lidar_state

        cs = digitalio.DigitalInOut(cs)
        rst = digitalio.DigitalInOut(rst)
        self._rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)

    @property
    def state(self):
        return self._state

    def dispatch(self):
        # Receive incoming messages from the ground. The only messages expected
        # from the ground are binary `command` messages that determine
        # orientation.
        for _ in range(MAX_MESSAGES):
            message = self._rfm95w.receive(timeout=0)
            if message is None:
                break
            self._handle_message(message)

        # Send an outgoing telemetry message to the ground.
        # Telemetry includes orientation, LiDaR, and temperature.

    def _handle_message(self, message: bytearray):
        command = int.from_bytes(command, byteorder="big")
        self._state.command = command
