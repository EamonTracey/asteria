import time

import adafruit_rfm9x
import board
import busio
import digitalio


def main():
    # Send.
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.CE1)
    rst = digitalio.DigitalInOut(board.D25)
    rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)

    print("ALL INITIALIZED.")

    count = 0
    while True:
        count += 1
        message = f"{count} Hello, Asteria!".encode()
        rfm95w.send(message)
        print(message)
        time.sleep(1)


if __name__ == "__main__":
    main()
