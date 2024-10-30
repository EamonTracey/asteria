import time
import board
import busio
import colorama

class GarminLidarLiteV4:
    def __init__(self, i2c, address=0x62):
        self.i2c = i2c
        self.address = address

    def write_register(self, reg, value):
        # Write a byte to a specific register
        # Create a byte array for the register and value
        data = bytes([reg, value])
        self.i2c.writeto(self.address, data)

    def read_register(self, reg, num_bytes=1):
        # Write the register we want to read, then read the response
        self.i2c.writeto(self.address, bytes([reg]))
        result = bytearray(num_bytes)
        self.i2c.readfrom_into(self.address, result)
        return result

    def trigger_measurement(self):
        # Step 1: Write 0x04 to register 0x00 to start measurement
        self.write_register(0x00, 0x04)

    def is_measurement_complete(self):
        # Step 2-3: Check if measurement is complete by reading 0x01 until LSB goes low
        status = self.read_register(0x01)[0]
        return (status & 0x01) == 0

    def read_distance(self):
        # Step 4: Read two bytes from 0x10 (low byte) and 0x11 (high byte)
        low_byte = self.read_register(0x10)[0]
        high_byte = self.read_register(0x11)[0]
        # Combine bytes into a 16-bit value
        distance = (high_byte << 8) | low_byte
        return distance

    def get_distance(self):
        # Trigger measurement and wait for completion
        self.trigger_measurement()
        while not self.is_measurement_complete():
            time.sleep(0.01)  # Sleep briefly to avoid overloading the I2C bus
        return self.read_distance()

# Example usage:
i2c = busio.I2C(board.SCL, board.SDA)
lidar = GarminLidarLiteV4(i2c)


try:
    while True:
        distance = lidar.get_distance()
        time.sleep(0.1)  # Take readings at 1-second intervals
        if distance < 5:
            print(f"{colorama.Fore.RED} CLOSE BY ({distance}cm)")
        else:
            print(f"{colorama.Fore.GREEN} FAR WAY ({distance}cm)")

except KeyboardInterrupt:
    print("Measurement stopped by user.")

