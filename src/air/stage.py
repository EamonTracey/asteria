from dataclasses import dataclass
import logging
from typing import Optional

from air.lidar import LidarState
from base.component import Component
from base.loop import LoopState

logger = logging.getLogger(__name__)

ZERO_TO_ONE_TRANSITION_TIME = 5  # s
ZERO_TO_ONE_TRANSITION_PROXIMITY = 500  # cm
ONE_TO_TWO_TRANSITION_TIME = 3  # s
ONE_TO_TWO_TRANSITION_PROXIMITY = 400  # cm


@dataclass
class StageState:
    # 0 -> flight has not begun
    # 1 -> in flight
    # 2 -> landing or landed
    stage: int = 0

    zero_to_one_transition_time: Optional[int] = None
    one_to_two_transition_time: Optional[int] = None


class StageComponent(Component):

    def __init__(self, loop_state: LoopState, lidar_state: LidarState):
        self._state = StageState()

        self._loop_state = loop_state
        self._lidar_state = lidar_state

    @property
    def state(self):
        return self._state

    def dispatch(self):
        stage = self._state.stage

        logger.info(f"{self._state.stage=}")

        if stage == 0:
            if self._state.zero_to_one_transition_time is None:
                if self._lidar_state.proximity >= ZERO_TO_ONE_TRANSITION_PROXIMITY:
                    self._state.zero_to_one_transition_time = self._loop_state.time
            else:
                if self._lidar_state.proximity >= ZERO_TO_ONE_TRANSITION_PROXIMITY:
                    if self._loop_state.time - self._state.zero_to_one_transition_time >= ZERO_TO_ONE_TRANSITION_TIME:
                        logger.info("Transitioning from stage 0 to stage 1")
                        self.stage = 1
                else:
                    self._state.zero_to_one_transition_time = None

        elif stage == 1:
            if self._state.one_to_two_transition_time is None:
                if self._lidar_state.proximity <= ONE_TO_TWO_TRANSITION_PROXIMITY:
                    self._state.one_to_two_transition_time = self._loop_state.time
            else:
                if self._lidar_state.proximity <= ONE_TO_TWO_TRANSITION_PROXIMITY:
                    if self._loop_state.time - self._state.one_to_two_transition_time >= ONE_TO_TWO_TRANSITION_TIME:
                        logger.info("Transitioning from stage 1 to stage 2")
                        self.stage = 2
                else:
                    self._state.one_to_two_transition_time = None

        elif stage == 2:
            ...
