import time

import adafruit_rfm9x
import board
import busio
import digitalio



def main():
    # Receive.
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.CE1)
    rst = digitalio.DigitalInOut(board.D14)
    rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)

    print("ALL INITIALIZED.")

    while True:
        message = rfm95w.receive(timeout=0)
        if message is not None:
            print(message)

        time.sleep(1)

if __name__ == "__main__":
    main()
