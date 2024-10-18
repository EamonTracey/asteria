import board
import busio

import adafruit_bno08x as bno08x
import adafruit_rfm9x as rfm9x

# Initialize and calibrate our devices.
i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c, debug=False)

def receive_data():
    ...

def update_state_goal():
    ...

def read_sensors():
    ...

def determine_state():
    ...

def perform_control():
    ...
