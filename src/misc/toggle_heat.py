from gpiozero import LED
from time import sleep

# Define GPIO pin 1i8 as an output pin
gpio_pin = LED(27)

try:
    while True:
        print("GPIO 27 HIGH")
        gpio_pin.on()  # Turn the pin HIGH
        sleep(10)  # Wait for 1 second

        print("GPIO 27 LOW")
        gpio_pin.off()  # Turn the pin LOW
        sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    print("\nExiting program...")
    gpio_pin.off()  # Ensure the pin is turned off
