import RPi.GPIO as GPIO
import time

# Set up the GPIO library
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(1, GPIO.OUT)  # Set GPIO 1 as an output pin

# Turn the GPIO pin on
GPIO.output(1, GPIO.HIGH)

# Keep the pin on for a while (optional)
time.sleep(60)  # Keeps the pin on for 10 seconds

# Clean up GPIO setup (best practice)
GPIO.cleanup()
