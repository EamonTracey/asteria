import adafruit_rfm9x
import board
import busio
import digitalio

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
rst = digitalio.DigitalInOut(board.D6)
rfm95w = adafruit_rfm9x.RFM9x(spi, cs, rst, 915)

while True:
    command = input("Send a command (0=minimum 1=maximum 2=medium): ")
    if command.lower() in ["q", "quit", "exit"]:
        break
    if command not in ["0", "1", "2"]:
        print("Error: please enter 0, 1, or 2.")
        continue
    command = int(command).to_bytes(1, byteorder="big")
    rfm95w.send(command)
