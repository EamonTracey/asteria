import adafruit_rfm9x
import board
import busio
import digitalio

from base.component import Component
from base.loop import Loop


class SendComponent(Component):

    def __init__(self, rfm95w: adafruit_rfm9x.RFM9x):
        self._rfm95w = rfm95w

        self._count = 0

    def dispatch(self):
        self._count += 1
        self._rfm95w.send(f"Hello, Asteria! {self._count}".encode())


def main():
    loop = Loop(1)

    # Send.
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.CE1)
    rst = digitalio.DigitalInOut(board.D14)
    rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)
    send_component = SendComponent(rfm95w)
    loop.add_component(send_component, 1)

    loop.run(0)


if __name__ == "__main__":
    main()
