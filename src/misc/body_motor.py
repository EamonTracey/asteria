import board
import pwmio
import time
import board

# Servo configuration
SERVO_FREQUENCY = 50  # 50 Hz for standard servo
SERVO_MINIMUM_PULSE_WIDTH = 0.001  # Minimum pulse width in seconds (1 ms)
SERVO_MAXIMUM_PULSE_WIDTH = 0.002  # Maximum pulse width in seconds (2 ms)

# Calculate duty cycles
duty_cycle_minimum = int(SERVO_MINIMUM_PULSE_WIDTH * SERVO_FREQUENCY * 2**16)
duty_cycle_maximum = int(SERVO_MAXIMUM_PULSE_WIDTH * SERVO_FREQUENCY * 2**16)

# Create a PWMOut object on GPIO26
pwm = pwmio.PWMOut(board.D26,
                   frequency=SERVO_FREQUENCY,
                   variable_frequency=False)


def set_angle(angle):
    """Set the servo to a specific angle (0 to 180)."""
    duty_cycle = int(
        (SERVO_MINIMUM_PULSE_WIDTH + (angle / 180) *
         (SERVO_MAXIMUM_PULSE_WIDTH - SERVO_MINIMUM_PULSE_WIDTH)) *
        SERVO_FREQUENCY * 2**16)
    pwm.duty_cycle = duty_cycle
    time.sleep(0.5)  # Allow the servo to reach the position


try:
    while True:
        # Iteratively rotate servo
        for angle in range(0, 181, 30):  # From 0° to 180° in steps of 30°
            print(f"Rotating to {angle}°")
            set_angle(angle)
            time.sleep(1)

        for angle in range(180, -1,
                           -30):  # From 180° back to 0° in steps of 30°
            print(f"Rotating to {angle}°")
            set_angle(angle)
            time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    pwm.deinit()
