from dataclasses import dataclass
import logging

import microcontroller
import pwmio

from base.component import Component
from air.bno085 import BNO085State
from air.rfm95w import RFM95WState

SERVO_FREQUENCY = 50
SERVO_MINIMUM_PULSE_WIDTH = 0.001
SERVO_MAXIMUM_PULSE_WIDTH = 0.002

logger = logging.getLogger(__name__)


@dataclass
class ControlState:
    duty_cycle: int = 0


class ControlComponent(Component):

    def __init__(self, pwm: microcontroller.Pin, bno085_state: BNO085State,
                 air_rfm95w_state: RFM95WState):
        self._state = ControlState()

        self._bno085_state = bno085_state
        self._air_rfm95w_state = air_rfm95w_state

        self._pwm = pwmio.PWMOut(pwm,
                                 frequency=SERVO_FREQUENCY,
                                 variable_frequency=False)

    @property
    def state(self):
        return self._state

    def dispatch(self):
        # TODO?: Implement controller.

        command = self._air_rfm95w_state.command

        if command == 0:
            # Minimum position.
            self._state.duty_cycle = int(SERVO_MINIMUM_PULSE_WIDTH *
                                         SERVO_FREQUENCY * 2**16)
        elif command == 1:
            # Maximum position.
            self._state.duty_cycle = int(SERVO_MAXIMUM_PULSE_WIDTH *
                                         SERVO_FREQUENCY * 2**16)
        elif command == 2:
            # Center position.
            self._state.duty_cycle = int(
                ((SERVO_MINIMUM_PULSE_WIDTH + SERVO_MAXIMUM_PULSE_WIDTH) / 2) *
                SERVO_FREQUENCY * 2**16)
        else:
            logger.info(f"Unknown command received: {command}")

        self._pwm.duty_cycle = self._state.duty_cycle
