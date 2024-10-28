from dataclasses import dataclass

import microcontroller
import pwmio

from base.component import Component
from air.bno085 import BNO085State
from air.rfm95w import AirRFM95WState

SERVO_FREQUENCY = 50
SERVO_MINIMUM_PULSE_WIDTH = 0.001
SERVO_MAXIMUM_PULSE_WIDTH = 0.002


@dataclass
class ControlState:
    duty_cycle: int = 0


class ControlComponent(Component):

    def __init__(self, pwm: microcontroller.Pin, bno085_state: BNO085State,
                 rfm95w_state: AirRFM95WState):
        self._state = ControlState()

        self._pwm = pwmio.PWMOut(pwm,
                                 frequency=FREQUENCY,
                                 variable_frequency=False)
        self._bno085_state = bno085_state
        self._rfm95w_state = rfm95w_state

    @property
    def state(self):
        return self._state

    def dispatch(self):
        # TODO: Implement controller.

        command = self._rfm95w_state.command
        if command is None:
            return

        if command == 0:
            self._state.duty_cycle = int(SERVO_MINIMUM_PULSE_WIDTH *
                                         SERVO_FREQUENCY * 2**16)
        elif command == 1:
            self._state.duty_cycle = int(SERVO_MAXIMUM_PULSE_WIDTH *
                                         SERVO_FREQUENCY * 2**16)

        self._pwm.duty_cycle = self._state.duty_cycle
