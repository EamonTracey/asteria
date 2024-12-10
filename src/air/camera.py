import logging
import os
import traceback

from picamera import PiCamera

from base.component import Component
from base.loop import LoopState

logger = logging.getLogger(__name__)


class CameraState:
    photos: int = 0

    last_photo_time: int = 0


class CameraComponent(Component):

    def __init__(self, period: float, loop_state: LoopState):
        self._state = CameraState()

        self._period = period
        self._loop_state = loop_state

        self._camera = PiCamera()
        logger.info("Camera initialized.")

    @property
    def state(self):
        return self._state

    def dispatch(self):
        if (loop_state.time - self._state.last_photo_time) < self._period:
            continue
        self._state.last_photo_time = loop_state.time

        try:
            path = f"photo_{photos}.jpg"
            self.camera.capture(path)
            self._state.photos += 1
        except Exception as exception:
            logger.exception(
                f"Exception when taking picamera photo: {traceback.format_exc()}"
            )
