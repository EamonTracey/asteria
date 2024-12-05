import adafruit_rfm9x
import board
import busio
import digitalio

from base.component import Component
from base.loop import Loop


class ReceiveComponent(Component):

    def __init__(self, rfm95w: adafruit_rfm9x.RFM9x):
        self._rfm95w = rfm95w

    def dispatch(self):
        message = self._rfm95w.receive(timeout=0)
        if message is not None:
            print(message.decode())


def main():
    loop = Loop(1)

    # Receive.
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.CE1)
    rst = digitalio.DigitalInOut(board.D14)
    rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)
    receive_component = ReceiveComponent(rfm95w)
    loop.add_component(receive_component, 1)

    loop.run(0)


if __name__ == "__main__":
    main()
