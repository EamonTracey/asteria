import smbus
import time


class LidarLiteComponent:
    LIDAR_I2C_ADDR = 0x62  # Default I2C address for LIDAR-Lite v4 LED
    DISTANCE_REGISTER = 0x8f  # Register for reading distance
    COMMAND_REGISTER = 0x00  # Register to initiate measurement
    MEASURE_COMMAND = 0x04  # Command to start distance measurement

    def __init__(self, bus_number=1):
        """
        Initializes the LidarLiteComponent, which communicates with the LIDAR sensor over I2C.
        :param bus_number: The I2C bus number (default is 1 for Raspberry Pi).
        """
        self.bus = smbus.SMBus(bus_number)

    def measure_distance(self):
        """
        Triggers a distance measurement and reads the result.
        :return: Measured distance in centimeters.
        """
        # Send command to take a distance measurement
        self.bus.write_byte_data(self.LIDAR_I2C_ADDR, self.COMMAND_REGISTER, self.MEASURE_COMMAND)
        time.sleep(0.02)  # Wait for measurement to be taken (20 ms)

        # Read the measured distance from the LIDAR
        high_byte = self.bus.read_byte_data(self.LIDAR_I2C_ADDR, self.DISTANCE_REGISTER)
        low_byte = self.bus.read_byte_data(self.LIDAR_I2C_ADDR, self.DISTANCE_REGISTER + 1)
        distance = (high_byte << 8) + low_byte
        return distance

    def alert_if_near_ground(self, threshold=50):
        """
        Measures the distance and prints an alert if below the threshold.
        :param threshold: Distance threshold in cm (default is 500 cm).
        """
        distance = self.measure_distance()
        if distance <= threshold:
            print(f"ALERT: Distance is {distance} cm, which is below the threshold of {threshold} cm!")
        else:
            print(f"Distance is {distance} cm.")


# Example usage
if __name__ == "__main__":
    lidar = LidarLiteComponent()
    while True:
        lidar.alert_if_near_ground()
        time.sleep(0.5)  # Delay between readings
