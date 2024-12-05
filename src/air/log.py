import csv
from dataclasses import dataclass

from base.component import Component
from base.loop import LoopState
from air.bno085 import BNO085State
from air.lidar import LidarState
from air.mcp9808 import MCP9808State
from air.stage import StageState

HEADERS = [
    "Time", "Loop_Slip_Count", "Acceleration_X_BNO085",
    "Acceleration_Y_BNO085", "Acceleration_Z_BNO085", "Magnetic_X_BNO085",
    "Magnetic_Y_BNO085", "Magnetic_Z_BNO085", "Gyro_X_BNO085", "Gyro_Y_BNO085",
    "Gyro_Z_BNO085", "Quaternion_W_BNO085", "Quaternion_X_BNO085",
    "Quaternion_Y_BNO085", "Quaternion_Z_BNO085", "Proximity_Lidar",
    "Temperature_MCP9808", "Acceleration_Errors_BNO085",
    "Magnetic_Errors_BNO085", "Gyro_Errors_BNO085", "Proximity_Errors_Lidar",
    "Temperature_Errors_MCP9808", "Stage"
]


@dataclass
class LogState:
    ...


class LogComponent(Component):

    def __init__(self, path: str, loop_state: LoopState,
                 bno085_state: BNO085State, lidar_state: LidarState,
                 mcp9808_state: MCP9808State, stage_state: StageState):
        self._state = LogState()

        self._loop_state = loop_state
        self._bno085_state = bno085_state
        self._lidar_state = lidar_state
        self._mcp9808_state = mcp9808_state
        self._stage_state = stage_state

        self._file = open(path, "w")
        self._writer = csv.writer(self._file)
        self._writer.writerow(HEADERS)

    def dispatch(self):
        record = [
            self._loop_state.time - self._loop_state.first_time,
            self._loop_state.slip_count,
            *self._bno085_state.acceleration,
            *self._bno085_state.magnetic,
            *self._bno085_state.gyro,
            *self._bno085_state.quaternion,
            self._lidar_state.proximity,
            self._mcp9808_state.temperature,
            self._bno085_state.acceleration_errors,
            self._bno085_state.magnetic_errors,
            self._bno085_state.gyro_errors,
            self._lidar_state.proximity_errors,
            self._mcp9808_state.temperature_errors,
            self._stage_state.stage,
        ]
        self._writer.writerow(record)
        self._file.flush()
