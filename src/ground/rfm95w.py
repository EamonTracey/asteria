from dataclasses import dataclass
import math

import adafruit_rfm9x
import busio
import digitalio
import microcontroller

from base.component import Component
from ground.command import CommandState


@dataclass
class RFM95WState:
    messages: int = 0


class RFM95WComponent(Component):

    def __init__(self, spi: busio.SPI, cs: microcontroller.Pin,
                 rst: microcontroller.Pin, command_state: CommandState):
        self._state = RFM95WState()

        self._command_state = command_state

        cs = digitalio.DigitalInOut(cs)
        rst = digitalio.DigitalInOut(rst)
        self._rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)

    @property
    def state(self):
        return self._state

    def dispatch(self):
        command = self._command_state.command

        if command is None:
            return

        command = command.to_bytes(math.ceil(command.bit_length()),
                                   byteorder="big")
        self._rfm95w.send(command)
