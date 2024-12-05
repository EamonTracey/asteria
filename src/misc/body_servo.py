import board
import pwmio
import time

# Servo configuration
SERVO_FREQUENCY = 333  # Operating frequency for LW-20MG (333 Hz)
SERVO_MINIMUM_PULSE_WIDTH = 0.0005  # Further expanded minimum pulse width (0.6 ms)
SERVO_MAXIMUM_PULSE_WIDTH = 0.0028  # Further expanded maximum pulse width (2.4 ms)

# Calculate duty cycles
duty_cycle_minimum = int(SERVO_MINIMUM_PULSE_WIDTH * SERVO_FREQUENCY * 2**16)
duty_cycle_maximum = int(SERVO_MAXIMUM_PULSE_WIDTH * SERVO_FREQUENCY * 2**16)

# Create a PWMOut object on GPIO12
pwm = pwmio.PWMOut(board.D12, frequency=SERVO_FREQUENCY)


def set_angle(angle):
    """Set the servo to a specific angle (0 to 180)."""
    if angle < 0 or angle > 180:
        print("Error: Angle out of range (0-180°)")
        return
    duty_cycle = int(
        (SERVO_MINIMUM_PULSE_WIDTH + (angle / 180) *
         (SERVO_MAXIMUM_PULSE_WIDTH - SERVO_MINIMUM_PULSE_WIDTH)) *
        SERVO_FREQUENCY * 2**16)
    print(f"Setting angle to {angle}°, Duty Cycle: {duty_cycle}")
    pwm.duty_cycle = duty_cycle
    time.sleep(0.5)  # Allow servo to reach position


try:
    while True:
        # Test full range
        print("Testing full range...")
        set_angle(0)  # Move to 0°
        time.sleep(2)
        set_angle(180)  # Move to 180°
        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    pwm.deinit()
