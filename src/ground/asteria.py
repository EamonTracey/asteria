import adafruit_rfm9x
import adafruit_ssd1306
import board
import busio
import digitalio

from base.loop import Loop
from ground.buttons import ButtonsComponent
from ground.proxy import ProxyComponent


class Asteria:

    def __init__(self, name, host: tuple[str, int], port: int):
        self._loop = Loop(10)

        # Connect to the I2C and SPI bus.
        i2c = board.I2C()
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        # Display.
        display = adafruit_ssd1306.SSD1306_I2C(128,
                                               32,
                                               i2c,
                                               reset=digitalio.DigitalInOut(
                                                   board.D4))
        width, height = display.width, display.height
        display.fill(0)
        display.text("Asteria", 0, 0, 1)
        display.text("Ground Station", 0, height // 2, 1)
        display.show()

        # Initialize the RFM95W.
        cs = digitalio.DigitalInOut(board.CE1)
        rst = digitalio.DigitalInOut(board.D25)
        rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)

        # Proxy.
        proxy_component = ProxyComponent(host, port, rfm95w)
        self._loop.add_component(proxy_component, 10)

        # Buttons.
        buttons_component = ButtonsComponent(rfm95w, board.D5, board.D6,
                                             board.D12)
        self._loop.add_component(buttons_component, 10)

    def run(self, steps: int):
        self._loop.run(steps)
