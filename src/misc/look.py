import smbus2
import time

I2C_BUS = 1
bus = smbus2.SMBus(I2C_BUS)

for address in range(0x03, 0x78):
    try:
        bus.read_byte(address)
        print(f"Device found at address: {hex(address)}")
    except Exception:
        pass

bus.close()
