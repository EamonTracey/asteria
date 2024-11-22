import socket
import sys
import time

from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import QTimer, QThread, pyqtSignal


class Asteria(QMainWindow):

    def __init__(self, name: str, ground: tuple[str, int], port: int):
        super().__init__()

        self.name = name
        self._ground = ground

        self.orientation = "-"
        self.temperature = "-"
        self.distance = "-"

        # Initialize the GUI
        self.init_ui()

        # Start telemetry updates in a separate thread
        self.telemetry_thread = TelemetryThread(port)
        self.telemetry_thread.update_telemetry.connect(self.update_telemetry)
        self.telemetry_thread.start()

    def init_ui(self):
        self.setWindowTitle(f"{self.name}")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)

        # Telemetry display
        telemetry_layout = QVBoxLayout()
        telemetry_label = QLabel("Asteria Ground Station", self)
        telemetry_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        telemetry_layout.addWidget(telemetry_label)

        self.orientation_label = QLabel(f"Orientation: {self.orientation}",
                                        self)
        self.temperature_label = QLabel(f"Temperature: {self.temperature}",
                                        self)
        self.distance_label = QLabel(f"Distance: {self.distance}", self)

        telemetry_layout.addWidget(self.orientation_label)
        telemetry_layout.addWidget(self.temperature_label)
        telemetry_layout.addWidget(self.distance_label)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        telemetry_layout.addItem(spacer)

        main_layout.addLayout(telemetry_layout)

        # Command buttons
        #command_layout = QHBoxLayout()
        #self.command_buttons = []
        #for i in range(3):
        #    button = QPushButton(f"Command {i + 1}", self)
        #    button.clicked.connect(lambda _, idx=i + 1: self.send_command(idx))
        #    command_layout.addWidget(button)
        #    self.command_buttons.append(button)
        #main_layout.addLayout(command_layout)

        self.setCentralWidget(central_widget)

    def send_command(self):
        ...

    def update_telemetry(self, telemetry: bytes):
        ...

    def run(self):
        self.show()


class TelemetryThread(QThread):
    update_telemetry = pyqtSignal(tuple)

    def __init__(self, port: int):
        super().__init__()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(("0.0.0.0", port))

    def run(self):
        while True:
            telemetry, _ = self._socket.recvfrom(4096)
            self.update_telemetry.emit(telemetry)
