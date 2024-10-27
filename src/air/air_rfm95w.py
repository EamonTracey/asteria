from dataclasses import dataclass

import busio
import digitalio
import adafruit_rfm9x

from base.component import Component
from base.message import Message


@dataclass
class AirRFM95WState:
    message: Optional[Message] = None


class AirRFM95WComponent(Component):

    def __init__(self, spi: busio.SPI, cs: digitalio.DigitialInOut,
                 rst: digitalio.DigitalInOut):
        self._state = AirRFM95WState()

        self._rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)

    @property
    def state(self):
        return self._state

    def dispatch(self):
        # TODO: Enhanced, error-resistant message parsing.

        message = self._rfm95w.receive(timeout=0)
        if message is not None:
            message = int.from_bytes(message, byteorder="big")
            self._state.message = Message(message)
