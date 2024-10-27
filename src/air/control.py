from dataclasses import dataclass

import microcontroller
import pwmio

from base.component import Component
from base.message import Message
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

        message = self._rfm95w_state.message
        if message is None:
            return

        if message == Message.ORIENTATION_ONE:
            self._state.duty_cycle = int(SERVO_MINIMUM_PULSE_WIDTH *
                                         SERVO_FREQUENCY * 2**16)
        elif message == Message.ORIENTATION_TWO:
            self._state.duty_cycle = int(SERVO_MAXIMUM_PULSE_WIDTH *
                                         SERVO_FREQUENCY * 2**16)

        self._pwm.duty_cycle = self._state.duty_cycle
