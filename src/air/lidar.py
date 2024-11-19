from dataclasses import dataclass
import logging
import time

import board
import busio

from base.component import Component

logger = logging.getLogger(__name__)


@dataclass
class LidarState:
    # Proximity to some nearby object in meters.
    proximity: int = 0

    # Count the number of times each reading fails.
    proximity_errors: int = 0


class LidarComponent(Component):

    def __init__(self, i2c: busio.I2C, address: int = 0x62):
        self._state = LidarState()

        self._i2c = i2c
        self._address = address

    @property
    def state(self):
        return self._state

    def dispatch(self):
        proximity = None
        try:
            proximity = self._get_proximity()
        except Exception as exception:
            logger.exception(
                f"Exception when reading LiDaR proximity: {traceback.format_exc()}"
            )
        if proximity is not None:
            self._state.proximity = proximity
        else:
            self._state.proximity_errors += 1

    def _write_register(self, reg: int, value: int):
        data = bytes([reg, value])
        self._i2c.writeto(self._address, data)

    def _read_register(self, reg: int, num_bytes: int = 1):
        self._i2c.writeto(self._address, bytes([reg]))
        result = bytearray(num_bytes)
        self._i2c.readfrom_into(self._address, result)
        return result

    def _is_measurement_complete(self) -> bool:
        status = self._read_register(0x01)[0]
        return (status & 0x01) == 0

    def _get_proximity(self) -> int:
        self._write_register(0x00, 0x04)
        while not self._is_measurement_complete():
            time.sleep(0.01)

        low_byte = self._read_register(0x10)[0]
        high_byte = self._read_register(0x11)[0]
        proximity = (high_byte << 8) | low_byte

        return proximity
