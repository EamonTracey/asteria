import logging
import os
import traceback

from picamera import PiCamera

from base.component import Component
from base.loop import LoopState

logger = logging.getLogger(__name__)


class CameraState:
    photos: int = 0


class CameraComponent(Component):

    def __init__(self, period: int, loop_state: LoopState):
        self._state = CameraState()
        self._counter = 0

        self._period = period
        self._loop_state = loop_state

        self._camera = PiCamera(resolution=(1280, 720))
        logger.info("Camera initialized.")

    @property
    def state(self):
        return self._state

    def dispatch(self):
        if self._counter % self._period == 0:
            try:
                path = f"photo_{self._state.photos}.jpg"
                self._camera.capture(path)
                logger.info(f"Captured photo {self._state.photos}.")
                self._state.photos += 1
            except Exception as exception:
                logger.exception(
                    f"Exception when taking picamera photo: {traceback.format_exc()}"
                )

        self._counter += 1
