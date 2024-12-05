import RPi.GPIO as GPIO
import time

# Pin configuration
GPIO_PIN = 18

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(GPIO_PIN, GPIO.OUT)

try:
    while True:
        # on for 5
        print("Turning on")
        GPIO.output(GPIO_PIN, GPIO.HIGH)  # Turn on
        time.sleep(5)  # Wait for 5 second
        GPIO.output(GPIO_PIN, GPIO.LOW)  # Turn off
        # off for 1
        print("Turning off")
        time.sleep(1)  # Wait for 1 second
except KeyboardInterrupt:
    print("\nExiting program")
finally:
    GPIO.cleanup()  # Clean up GPIO states on exit
