import board
import busio
import digitalio

from base.loop import Loop
from air.air_rfm95w import AirRFM95WComponent
from air.bno085 import BNO085Component
from air.lidar_lite import LidarLiteComponent
from air.mcp9808 import MCP9808Component
from air.picamera import PiCameraComponent


class AirAsteria:

    def __init__(self):
        self._loop = Loop(1)

        # Connect to the I2C and SPI buses.
        i2c = board.I2C()
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        # BNO085.
        bno085_component = BNO085Component(i2c)
        self._loop.add_component(bno085_component, 1)

        # MCP9808.
        mcp9808_component = MCP9808Component(i2c)
        self._loop.add_component(mcp9808_component, 1)

        # Air RFM95W.
        air_rfm95w_component = AirRFM95WComponent(spi, board.D5, board.D6)
        self._loop.add_component(air_rfm95w_component, 1)

        # PiCamera Component.
        picamera_component = PiCameraComponent()
        self._loop.add_component(picamera_component, 1)

        # Lidar Component.
        lidar_component = LidarLiteComponent(i2c)
        self._loop.add_component(lidar_component, 2)

    def run(self, steps: int):
        self._loop.run(steps)
