import smbus2

I2C_BUS = 1  # Default I2C bus on Raspberry Pi
bus = smbus2.SMBus(I2C_BUS)

print("Scanning all I2C addresses...")
for address in range(0x03, 0x78):
    try:
        bus.read_byte(address)
        print(f"Device found at address: {hex(address)}")
    except Exception:
        pass

bus.close()
