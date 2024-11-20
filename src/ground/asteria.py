import board
import busio
import digitalio

from base.loop import Loop
from ground.proxy import ProxyComponent


class Asteria:

    def __init__(self, name, host: tuple[str, int], port: int):
        self._loop = Loop(1)

        # Connect to the SPI bus.
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        # Proxy.
        proxy_component = ProxyComponent(host, port, spi, board.CE1, board.D25)
        self._loop.add_component(proxy_component, 1)

    def run(self, steps: int):
        self._loop.run(steps)
