import time

import adafruit_mcp9808
import board

i2c = board.I2C()
mcp9808 = adafruit_mcp9808.MCP9808(i2c, 0x1C)

while True:
    print(f"Temperature (°C): {mcp9808.temperature}")
    time.sleep(1)
