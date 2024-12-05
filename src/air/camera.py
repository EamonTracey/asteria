from datetime import datetime
import os
import traceback

from picamera import PiCamera

from base.component import Component

logger = logging.getLogger(__name__)


class CameraState:
    photos: int = 0


class CameraComponent(Component):

    def __init__(self):
        self._state = CameraState()

        self._camera = PiCamera()

        logger.info("Camera initialized.")

    @property
    def state(self):
        return self._state

    def dispatch(self):
        try:
            path = f"photo_{photos}.jpg"
            self.camera.capture(path)
            self._state.photos += 1
        except Exception as exception:
            logger.exception(
                f"Exception when taking picamera photo: {traceback.format_exc()}"
            )
