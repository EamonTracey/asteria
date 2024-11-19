import datetime

import board
import busio
import digitalio

from base.loop import Loop
from air.rfm95w import RFM95WComponent
from air.bno085 import BNO085Component
from air.control import ControlComponent
from air.lidar import LidarComponent
from air.log import LogComponent
from air.mcp9808 import MCP9808Component
from air.temperature_regulation import TemperatureRegulationComponent


class Asteria:

    def __init__(self, name: str):
        # Loop!
        self._loop = Loop(1)

        # Naming is hard.
        utc_date = datetime.datetime.now(datetime.UTC)
        utc_date_string = utc_date.strftime("%Y%m%d%H%M%S")
        name = f"Asteria {utc_date_string}"

        # Connect to the I2C and SPI buses.
        i2c = board.I2C()
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        # BNO085.
        bno085_component = BNO085Component(i2c)
        bno085_state = bno085_component.state
        self._loop.add_component(bno085_component, 1)

        # RFM95W.
        rfm95w_component = RFM95WComponent(spi, board.D5, board.D6)
        rfm95w_state = rfm95w_component.state
        self._loop.add_component(rfm95w_component, 1)

        # Lidar .
        lidar_component = LidarComponent(i2c)
        self._loop.add_component(lidar_component, 1)

        # MCP9808.
        mcp9808_component = MCP9808Component(i2c)
        mcp9808_state = mcp9808_component.state
        self._loop.add_component(mcp9808_component, 1)

        # Temperature Regulation.
        temperature_regulation_component = TemperatureRegulationComponent(
            mcp9808_state)
        self._loop.add_component(temperature_regulation_component, 1)

        # Control.
        control_component = ControlComponent(board.D13, bno085_state,
                                             rfm95w_state)
        self._loop.add_component(control_component, 1)

        # Log
        log_component = LogComponent(f"{name}.csv}")
        self._loop.add_component(log_component, 1)

    def run(self, steps: int):
        self._loop.run(steps)
