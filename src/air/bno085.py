from dataclasses import dataclass

import adafruit_bno08x
import busio

from base.component import Component


@dataclass
class BNO085State:
    acceleration: tuple[float, float, float] = (0, 0, 0)
    magnetic: tuple[float, float, float] = (0, 0, 0)
    gyro: tuple[float, float, float] = (0, 0, 0)
    quaternion: tuple[float, float, float, float] = (0, 0, 0, 0)

    acceleration_readings: int = 0
    magnetic_readings: int = 0
    gyro_readings: int = 0
    quaternion_readings: int = 0


class BNO085Component(Component):

    def __init__(self, i2c: busio.I2C, address: int = 0x4a):
        self._state = BNO085State()

        self._bno085 = adafruit_bno08x.i2c.BNO08X_I2C(i2c, address)
        self._bno085.initialize()
        self._bno085.enable_feature(adafruit_bno08x.BNO_REPORT_ACCELEROMETER)
        self._bno085.enable_feature(adafruit_bno08x.BNO_REPORT_MAGNETOMETER)
        self._bno085.enable_feature(adafruit_bno08x.BNO_REPORT_GYROSCOPE)
        self._bno085.enable_feature(adafruit_bno08x.BNO_REPORT_ROTATION_VECTOR)
        self._bno085.begin_calibration()

    @property
    def state(self):
        return self._state

    def dispatch(self):
        acceleration = self._bno085.acceleration
        if acceleration is not None:
            self._state.acceleration = acceleration
            self._state.acceleration_readings += 1

        magnetic = self._bno085.magnetic
        if magnetic is not None:
            self._state.magnetic = magnetic
            self._state.magnetic_readings += 1

        gyro = self._bno085.gyro
        if gyro is not None:
            self._state.gyro = gyro
            self._state.gyro_readings += 1

        quaternion = self._bno085.quaternion
        if quaternion is not None:
            self._state.quaternion = quaternion
            self._state.quaternion_readings += 1
