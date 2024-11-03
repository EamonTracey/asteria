from dataclasses import dataclass
from typing import Optional

import adafruit_rfm9x
import busio
import digitalio
import microcontroller

from base.component import Component


@dataclass
class RFM95WState:
    command: Optional[int] = None


class RFM95WComponent(Component):

    def __init__(self, spi: busio.SPI, cs: microcontroller.Pin,
                 rst: microcontroller.Pin):
        self._state = RFM95WState()

        cs = digitalio.DigitalInOut(cs)
        rst = digitalio.DigitalInOut(rst)
        self._rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)

    @property
    def state(self):
        return self._state

    def dispatch(self):
        command = self._rfm95w.receive(timeout=0)

        if command is None:
            return

        command = int.from_bytes(command, byteorder="big")
        self._state.command = command
