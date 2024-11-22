from dataclasses import dataclass
import logging
import socket
import traceback

import adafruit_rfm9x
import digitalio
import microcontroller

from base.component import Component

logger = logging.getLogger(__name__)


@dataclass
class ButtonsState:
    ...


class ButtonsComponent(Component):

    def __init__(self, rfm95w: adafruit_rfm9x.RFM9x, pin1: microcontroller.Pin,
                 pin2: microcontroller.Pin, pin3: microcontroller.Pin):
        self._state = ButtonsState()

        self._rfm95w = rfm95w

        self._button1 = digitalio.DigitalInOut(pin1)
        self._button1.direction = digitalio.Direction.INPUT
        self._button1.pull = digitalio.Pull.UP
        self._button2 = digitalio.DigitalInOut(pin2)
        self._button2.direction = digitalio.Direction.INPUT
        self._button2.pull = digitalio.Pull.UP
        self._button3 = digitalio.DigitalInOut(pin3)
        self._button3.direction = digitalio.Direction.INPUT
        self._button3.pull = digitalio.Pull.UP

    @property
    def state(self):
        return self._state

    def dispatch(self):
        message = None
        if not self._button1.value:
            message = b"\x00"
        if not self._button2.value:
            message = b"\x01"
        if not self._button3.value:
            message = b"\x02"

        if message is not None:
            self._rfm95w.send(message)
            logger.info(f"Sent {message=} to air.")
