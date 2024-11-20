import board
import microcontroller
import pwmio

SERVO_FREQUENCY = 50
SERVO_MINIMUM_PULSE_WIDTH = 0.001
SERVO_MAXIMUM_PULSE_WIDTH = 0.002

duty_cycle_minimum = int(SERVO_MINIMUM_PULSE_WIDTH * SERVO_FREQUENCY * 2**16)
duty_cycle_maximum = int(SERVO_MAXIMUM_PULSE_WIDTH * SERVO_FREQUENCY * 2**16)
duty_cycle_center = int((SERVO_MINIMUM_PULSE_WIDTH + SERVO_MAXIMUM_PULSE_WIDTH) / 2 * SERVO_FREQUENCY * 2**16)

pwm = pwmio.PWMOut(board.D13, frequency=SERVO_FREQUENCY, variable_frequency=False)


while True:
    duty_cycle = input("Send a duty_cycle (0=minimum 1=maximum 2=medium): ")
    if duty_cycle.lower() in ["q", "quit", "exit"]:
        break
    if duty_cycle not in ["0", "1", "2"]:
        print("Error: please enter 0, 1, or 2.")
        continue
    duty_cycle = int(duty_cycle)
    pwm.duty_cycle = [duty_cycle_minimum, duty_cycle_maximum, duty_cycle_center][duty_cycle]
