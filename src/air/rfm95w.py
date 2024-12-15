from dataclasses import dataclass
import logging

import adafruit_rfm9x
import busio
import digitalio
import microcontroller

from air.bno085 import BNO085State
from air.lidar import LidarState
from air.mcp9808 import MCP9808State
from base.component import Component
from base.math import float_to_fixed_bytes

logger = logging.getLogger(__name__)

MAX_MESSAGES = 10


@dataclass
class RFM95WState:
    command: int = 0


class RFM95WComponent(Component):

    def __init__(self, spi: busio.SPI, cs: microcontroller.Pin,
                 rst: microcontroller.Pin, bno085_state: BNO085State,
                 lidar_state: LidarState, mcp9808_state: MCP9808State):
        self._state = RFM95WState()
        self._counter = 0

        self._bno085_state = bno085_state
        self._lidar_state = lidar_state
        self._mcp9808_state = mcp9808_state

        cs = digitalio.DigitalInOut(cs)
        rst = digitalio.DigitalInOut(rst)
        self._rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)

        logger.info("RFM95W initialized.")
        logger.info(f"{self._rfm95w.frequency_mhz=}")
        logger.info(f"{self._rfm95w.signal_bandwidth=}")
        logger.info(f"{self._rfm95w.spreading_factor=}")
        logger.info(f"{self._rfm95w.tx_power=}")
        logger.info(f"{self._rfm95w.xmit_timeout=}")

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
        # Telemetry includes quaternion, proximity, and temperature.
        if self._counter % 10 == 0:
            telemetry_serialized = self._generate_telemetry()
            logger.info(f"Sending {telemetry_serialized=}")
            self._rfm95w.send(telemetry_serialized)

        self._counter += 1

    def _handle_message(self, message: bytearray):
        logger.info(f"Received {message=}")
        command = int.from_bytes(bytes(message), byteorder="big")
        self._state.command = command

    def _generate_telemetry(self) -> bytes:
        quaternion = self._bno085_state.quaternion
        quaternion_serialized = bytes()
        for element in quaternion:
            quaternion_serialized += float_to_fixed_bytes(element, -1.0, 1.0)
        proximity = self._lidar_state.proximity
        proximity_serialized = float_to_fixed_bytes(proximity, 0, 1000.0)
        temperature = self._mcp9808_state.temperature
        temperature_serialized = float_to_fixed_bytes(temperature, -100.0,
                                                      100.0)
        telemetry_serialized = quaternion_serialized + proximity_serialized + temperature_serialized
        return telemetry_serialized
