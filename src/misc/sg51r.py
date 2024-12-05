import pwmio
from adafruit_motor import servo
import board
import time

SERVO_FREQUENCY = 50
SERVO_MINIMUM_PULSE_WIDTH = 750
SERVO_MAXIMUM_PULSE_WIDTH = 2500

pwm = pwmio.PWMOut(board.D13, frequency=SERVO_FREQUENCY)
sg51r_servo = servo.Servo(pwm,
                          min_pulse=SERVO_MINIMUM_PULSE_WIDTH,
                          max_pulse=SERVO_MAXIMUM_PULSE_WIDTH)
while True:
    sg51r_servo.angle = 0
    time.sleep(2)
    sg51r_servo.angle = 180
    time.sleep(2)
