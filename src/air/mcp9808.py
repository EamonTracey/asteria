from dataclasses import dataclass
import logging
import traceback

import adafruit_mcp9808
import busio

from base.component import Component

logger = logging.getLogger(__name__)


@dataclass
class MCP9808State:
    # Temperature in Celsius.
    temperature: float = 0

    # Count the number of times each reading fails.
    temperature_errors: int = 0


class MCP9808Component(Component):

    def __init__(self, i2c: busio.I2C, address: int = 0x18):
        self._state = MCP9808State()

        self._mcp9808 = adafruit_mcp9808.MCP9808(i2c, address=address)
        # self._mcp9808.resolution = 0

        logger.info("MCP9808 initialized.")
        logger.info(f"{self._mcp9808.upper_temperature=}")
        logger.info(f"{self._mcp9808.lower_temperature=}")
        logger.info(f"{self._mcp9808.critical_temperature=}")
        logger.info(f"{self._mcp9808.resolution=}")

    @property
    def state(self):
        return self._state

    def dispatch(self):
        temperature = None
        try:
            temperature = self._mcp9808.temperature
        except Exception as exception:
            logger.exception(
                f"Exception when reading MCP9808 temperature: {traceback.format_exc()}"
            )
        if temperature is not None:
            self._state.temperature = temperature
        else:
            self._state.temperature_errors += 1
