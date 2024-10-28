from dataclasses import dataclass

import adafruit_mcp9808
import busio

from base.component import Component


@dataclass
class MCP9808State:
    temperature: float = 0

    temperature_readings: int = 0


class MCP9808Component(Component):

    def __init__(self, i2c: busio.I2C, address: int = 0x18):
        self._state = MCP9808State()

        self._mcp9808 = adafruit_mcp9808.MCP9808(i2c)

    @property
    def state(self):
        return self._state

    def dispatch(self):
        temperature = self._mcp9808.temperature
        if temperature is not None:
            self._state.temperature = temperature
            self._state.temperature_readings += 1
