import time

import adafruit_rfm9x
import board
import busio
import digitalio

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.CE1)
rst = digitalio.DigitalInOut(board.D14)
while True:
    try:
        rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)
        break
    except Exception as exception:
        print("FAILURE")
    time.sleep(1)
print("SUCCESS")
