import board
import busio
import digitalio

from base.loop import Loop
from air.bno085 import BNO085Component


class AirAsteria:

    def __init__(self):
        self._loop = Loop(1)

        # Connect to the I2C and SPI buses.
        i2c = board.I2C()
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        # BNO085.
        bno085_component = BNO085Component(i2c)
        self._loop.add_component(bno085_component, i2c, 1)

        # Air RFM95W.
        air_rfm95w_component = AirRFM95WComponent(spi, board.D5, board.D6)
        self._loop.add_component(air_rfm95w_component, 1)

    def run(self, int: steps):
        self._loop.run(steps)
