import os
import time
from picamera import PiCamera
from datetime import datetime


class PiCameraComponent:

    def __init__(self, run_index: int):
        # Initialize the camera
        self.camera = PiCamera()

        # Create directory structure
        base_path = "/home/pi/Desktop/CameraMedia"
        self.run_folder = os.path.join(base_path, f"Testing_{run_index}")
        os.makedirs(self.run_folder, exist_ok=True)

    def capture_image(self):
        """Capture an image with a timestamped name."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.run_folder, f"image_{timestamp}.jpg")
        print(f"Starting to capture image: {output_path}")
        self.camera.start_preview()
        time.sleep(2)  # Give time for camera to adjust
        self.camera.capture(output_path)
        self.camera.stop_preview()
        print(f"Image saved to {output_path}")

    def record_video(self, duration: int = 5):
        """Record video for a given duration with a timestamped name."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.run_folder, f"video_{timestamp}.h264")
        print(
            f"Starting video recording: {output_path} for {duration} seconds")
        self.camera.start_preview()
        self.camera.start_recording(output_path)
        time.sleep(duration)
        self.camera.stop_recording()
        self.camera.stop_preview()
        print(f"Video saved to {output_path}")

    def close(self):
        """Safely close the camera."""
        print("Closing the camera.")
        self.camera.close()


# Main executable
if __name__ == "__main__":
    run_index = 1  # Update this index as needed for each run
    camera_component = PiCameraComponent(run_index)

    # Capture a few pictures with timestamped names
    for i in range(3):
        print(f"Capturing image {i + 1}")
        camera_component.capture_image()
        time.sleep(1)  # Short delay between captures

    # Record a video for 5 seconds with a timestamped name
    camera_component.record_video(5)

    # Close the camera
    camera_component.close()
