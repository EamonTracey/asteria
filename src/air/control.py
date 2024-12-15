from dataclasses import dataclass
import logging

import microcontroller
import pwmio

from base.component import Component
from air.bno085 import BNO085State
from air.rfm95w import RFM95WState
from air.stage import StageState

# LW-20MG servo motor specifications (benchtop tested).
BODY_SERVO_FREQUENCY = 333
BODY_SERVO_MINIMUM_PULSE_WIDTH = 0.0005
BODY_SERVO_MAXIMUM_PULSE_WIDTH = 0.0028

# SG51R servo motor specifications (benchtop tested).
LEG_SERVO_FREQUENCY = 50
LEG_SERVO_MINIMUM_PULSE_WIDTH = 0.00075
LEG_SERVO_MAXIMUM_PULSE_WIDTH = 0.0024

logger = logging.getLogger(__name__)


@dataclass
class ControlState:
    body_duty_cycle: int = 0
    leg_duty_cycle: int = 90


class ControlComponent(Component):

    def __init__(self, body_pwm: microcontroller.Pin,
                 leg_pwm: microcontroller.Pin, bno085_state: BNO085State,
                 air_rfm95w_state: RFM95WState, stage_state: StageState):
        self._state = ControlState()

        self._bno085_state = bno085_state
        self._air_rfm95w_state = air_rfm95w_state
        self._stage_state = stage_state

        self._body_pwm = pwmio.PWMOut(body_pwm,
                                      frequency=BODY_SERVO_FREQUENCY,
                                      variable_frequency=False)

        self._leg_pwm = pwmio.PWMOut(leg_pwm,
                                     frequency=LEG_SERVO_FREQUENCY,
                                     variable_frequency=False)

        logger.info("Servo motor PWM signals initialized.")
        logger.info(
            f"{BODY_SERVO_FREQUENCY=} {BODY_SERVO_MINIMUM_PULSE_WIDTH=} {BODY_SERVO_MAXIMUM_PULSE_WIDTH=}"
        )
        logger.info(
            f"{LEG_SERVO_FREQUENCY=} {LEG_SERVO_MINIMUM_PULSE_WIDTH=} {LEG_SERVO_MAXIMUM_PULSE_WIDTH=}"
        )
        logger.info(f"{self._body_pwm=}")
        logger.info(f"{self._leg_pwm=}")

    @property
    def state(self):
        return self._state

    def dispatch(self):
        stage = self._stage_state.stage

        # Perform body rotation.
        if stage == 0 or stage == 1:
            command = self._air_rfm95w_state.command
            if command == 0:
                # Minimum position.
                self._state.body_duty_cycle = int(
                    BODY_SERVO_MINIMUM_PULSE_WIDTH * BODY_SERVO_FREQUENCY *
                    2**16)
            elif command == 1:
                # Center position.
                self._state.body_duty_cycle = int(
                    ((BODY_SERVO_MINIMUM_PULSE_WIDTH +
                      BODY_SERVO_MAXIMUM_PULSE_WIDTH) / 2) *
                    BODY_SERVO_FREQUENCY * 2**16)
            elif command == 2:
                # Maximum position.
                self._state.body_duty_cycle = int(
                    BODY_SERVO_MAXIMUM_PULSE_WIDTH * BODY_SERVO_FREQUENCY *
                    2**16)
            else:
                logger.info(f"Unknown command received: {command}")

        # Perform leg deployment.
        if self._stage_state.stage == 2:
            # TODO: which way is which?
            ...

        # Set the duty cycles of the PWM signals.
        self._body_pwm.duty_cycle = self._state.body_duty_cycle
        self._leg_pwm.duty_cycle = self._state.leg_duty_cycle
