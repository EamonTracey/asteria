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
        self._loop.add_component(bno085_component, i2c)

        # Air RFM95W.
        air_rfm95w_cs = digitalio.DigitalInOut(board.D5)
        air_rfm95w_rst = digitalio.DigitalInOut(board.D6)
        air_rfm95w_component = AirRFM95WComponent(spi, air_rfm95w_cs,
                                                  air_rfm95w_rst)
        self._loop.add_component(air_rfm95w_component)

    def run(self, int: steps):
        self._loop.run(steps)
