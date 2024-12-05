import smbus2
import time

# Default I2C address of the LIDAR
DEFAULT_ADDRESS = 0x63
# New I2C address (replace 0x63 with the desired new address)
NEW_ADDRESS = 0x62

# I2C bus number (typically 1 on Raspberry Pi)
I2C_BUS = 1

# Register to change the I2C address
I2C_CHANGE_REGISTER = 0xEA

def change_i2c_address(bus, old_address, new_address):
    try:
        print(f"Changing I2C address from {hex(old_address)} to {hex(new_address)}")
        # Write the new address to the register
        bus.write_byte_data(old_address, I2C_CHANGE_REGISTER, new_address)
        time.sleep(0.1)  # Wait for the change to take effect
        print(f"Successfully changed I2C address to {hex(new_address)}")
    except Exception as e:
        print(f"Failed to change I2C address: {e}")

def main():
    # Create an SMBus instance
    bus = smbus2.SMBus(I2C_BUS)

    # Change the I2C address
    change_i2c_address(bus, DEFAULT_ADDRESS, NEW_ADDRESS)

    # Close the bus
    bus.close()

if __name__ == "__main__":
    main()
