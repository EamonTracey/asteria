import board
import pwmio
import time

# Servo configuration
SERVO_FREQUENCY = 50  # Standard servo frequency (50 Hz)
SERVO_MINIMUM_PULSE_WIDTH = 0.00035  # Minimum pulse width in seconds (0.35 ms)
SERVO_MAXIMUM_PULSE_WIDTH = 0.00265  # Maximum pulse width in seconds (2.65 ms)

# Calculate duty cycles
duty_cycle_minimum = int(SERVO_MINIMUM_PULSE_WIDTH * SERVO_FREQUENCY * 2**16)
duty_cycle_maximum = int(SERVO_MAXIMUM_PULSE_WIDTH * SERVO_FREQUENCY * 2**16)

# Create a PWMOut object on GPIO D13
pwm = pwmio.PWMOut(board.D13, frequency=SERVO_FREQUENCY)

def set_angle(angle):
    """Set the servo to a specific angle (0 to 180)."""
    if angle < 0 or angle > 180:
        print("Error: Angle out of range (0-180°)")
        return
    duty_cycle = int(
        (SERVO_MINIMUM_PULSE_WIDTH +
         (angle / 180) * (SERVO_MAXIMUM_PULSE_WIDTH - SERVO_MINIMUM_PULSE_WIDTH))
        * SERVO_FREQUENCY * 2**16
    )
    print(f"Setting angle to {angle}°, Duty Cycle: {duty_cycle}")
    pwm.duty_cycle = duty_cycle
    time.sleep(0.5)  # Allow servo to reach position

try:
    while True:
        # Move to 180°
        print("Moving to 180°")
        set_angle(180)

        # Pause at 180°
        print("Pausing at 180°")
        time.sleep(2)

        # Move back to 0°
        print("Moving to 0°")
        set_angle(0)

        # Pause at 0°
        print("Pausing at 0°")
        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    pwm.deinit()
