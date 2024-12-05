import board
import pwmio
import time

# Calculate duty cycles
duty_cycle = 1

# Create a PWMOut object on GPIO18
pwm = pwmio.PWMOut(board.D18, frequency=333)

def blink(angle):
    """Blink."""
    print(f"Blinking.\n")
    pwm.duty_cycle = duty_cycle
    time.sleep(2)  # Allow servo to reach position
    pwm.duty_cycle = 0

try:
    while True:
        # Test full range
        print("Testing GPIO pin...\n")
        blink(0)    # Move to 0°
        time.sleep(2)
       
except KeyboardInterrupt:
    print("Exiting program...")

finally:
    pwm.deinit()
