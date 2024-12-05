import datetime

import board
import busio
import digitalio

from base.loop import Loop
from air.rfm95w import RFM95WComponent
from air.rfm95w import RFM95WState
from air.bno085 import BNO085Component
from air.control import ControlComponent
from air.lidar import LidarComponent
from air.log import LogComponent
from air.mcp9808 import MCP9808Component
from air.temperature_regulation import TemperatureRegulationComponent
from air.stage import StageComponent
from air.camera import CameraComponent


class Asteria:

    def __init__(self, name: str):
        # Loop!
        self._loop = Loop(10)
        loop_state = self._loop.state

        # Connect to the I2C and SPI buses.
        i2c = board.I2C()
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        # BNO085.
        bno085_component = BNO085Component(i2c)
        bno085_state = bno085_component.state
        self._loop.add_component(bno085_component, 10)

        # Lidar.
        lidar_component = LidarComponent(i2c)
        lidar_state = lidar_component.state
        self._loop.add_component(lidar_component, 10)

        # MCP9808.
        mcp9808_component = MCP9808Component(i2c, 0x1C)
        mcp9808_state = mcp9808_component.state
        self._loop.add_component(mcp9808_component, 10)

        # RFM95W.
        rfm95w_component = RFM95WComponent(spi, board.CE1, board.D14,
                                           bno085_state, lidar_state,
                                           mcp9808_state)
        rfm95w_state = rfm95w_component.state
        self._loop.add_component(rfm95w_component, 2)

        # Temperature Regulation.
        temperature_regulation_component = TemperatureRegulationComponent(
            mcp9808_state)
        self._loop.add_component(temperature_regulation_component, 10)

        # Stage.
        stage_component = StageComponent(loop_state, lidar_state)
        stage_state = stage_component.state
        self._loop.add_component(stage_component, 10)

        # Control.
        control_component = ControlComponent(board.D12, board.D13,
                                             bno085_state, rfm95w_state,
                                             stage_state)
        self._loop.add_component(control_component, 10)

        # Camera.
        #camera_component = CameraComponent()
        #self._loop.add_component(camera_component, 1)

        # Log
        log_component = LogComponent(f"{name}.csv", loop_state, bno085_state,
                                     lidar_state, mcp9808_state, stage_state)
        self._loop.add_component(log_component, 10)

    def run(self, steps: int):
        self._loop.run(steps)
