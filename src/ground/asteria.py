import adafruit_rfm9x
import board
import busio
import digitalio

from base.loop import Loop
from ground.buttons import ButtonsComponent
from ground.proxy import ProxyComponent


class Asteria:

    def __init__(self, name, host: tuple[str, int], port: int):
        self._loop = Loop(1)

        # Connect to the SPI bus.
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        # Initialize the RFM95W.
        cs = digitalio.DigitalInOut(cs)
        rst = digitalio.DigitalInOut(rst)
        rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)

        # Proxy.
        proxy_component = ProxyComponent(host, port, rfm95w)
        self._loop.add_component(proxy_component, 1)

        # Buttons.
        buttons_component = ButtonsComponent(rfm95w, board.D5, board.D6,
                                             board.D12)
        self._loop.add_component(buttons_component, 1)

    def run(self, steps: int):
        self._loop.run(steps)
