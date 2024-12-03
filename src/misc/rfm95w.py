import adafruit_rfm9x
import board
import busio
import digitalio

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.CE0)
rst = digitalio.DigitalInOut(board.D14)
rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)
