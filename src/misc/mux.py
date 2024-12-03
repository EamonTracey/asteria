from smbus2 import SMBus
# Define the PCA9557 I2C address (replace with the actual address)
PCA9557_ADDR = 0x18
# Register addresses
CONFIG_REG = 0x03  # Configuration Register
OUTPUT_REG = 0x01  # Output Port Register


# Configure IO2 and IO6 as outputs
def configure_io2_io6(bus):
    # Read the current configuration register value
    config = bus.read_byte_data(PCA9557_ADDR, CONFIG_REG)
    # Clear bits 2 and 6 to set IO2 and IO6 as outputs
    new_config = config & ~(1 << 7) & ~(1 << 6)
    # Write the updated configuration back to the configuration register
    bus.write_byte_data(PCA9557_ADDR, CONFIG_REG, new_config)


# Set IO2 and IO6 HIGH
def set_io2_io6_high(bus):
    # Read the current output port register value
    output = bus.read_byte_data(PCA9557_ADDR, OUTPUT_REG)
    # Set bits 2 and 6 to make IO2 and IO6 HIGH
    new_output = output | (1 << 7) | (1 << 6)
    # Write the updated output back to the output port register
    bus.write_byte_data(PCA9557_ADDR, OUTPUT_REG, new_output)


# Main function
if __name__ == "__main__":
    # Open the I2C bus
    with SMBus(
            1
    ) as bus:  # Replace '1' with the correct I2C bus number for your setup
        configure_io2_io6(bus)  # Configure IO2 and IO6 as outputs
        set_io2_io6_high(bus)  # Set IO2 and IO6 HIGH
        print("IO2 and IO6 configured as outputs and set to HIGH")
