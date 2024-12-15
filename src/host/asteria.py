import logging
import socket
import sys
import time

import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem,
                             QSizePolicy)
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem
from stl import mesh
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from pyqtgraph.opengl import GLBoxItem

from base.math import fixed_bytes_to_float

logger = logging.getLogger(__name__)


class VisualizationWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asteria Visualization")

        self.vtkWidget = QVTKRenderWindowInteractor(self)
        layout = QVBoxLayout()
        layout.addWidget(self.vtkWidget)
        self.setLayout(layout)
        self.vtkWidget.GetRenderWindow().AddRenderer(vtk.vtkRenderer())
        self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer(
        ).SetBackground(0.1, 0.1, 0.1)
        self.vtkWidget.GetRenderWindow().GetInteractor().Initialize()
        self.vtkWidget.GetRenderWindow().GetInteractor().Start()
        self.load_stl("cad/Asteria_Outside_Body.stl")

    def load_stl(self, file_path):
        stl_mesh = mesh.Mesh.from_file(file_path)
        points = vtk.vtkPoints()
        cells = vtk.vtkCellArray()
        for triangle in stl_mesh.vectors:
            ids = []
            for vertex in triangle:
                point_id = points.InsertNextPoint(vertex)
                ids.append(point_id)
            cells.InsertNextCell(3, ids)

        poly_data = vtk.vtkPolyData()
        poly_data.SetPoints(points)
        poly_data.SetPolys(cells)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(poly_data)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        renderer = self.vtkWidget.GetRenderWindow().GetRenderers(
        ).GetFirstRenderer()
        renderer.AddActor(actor)
        renderer.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = STLViewer()
    window.show()
    sys.exit(app.exec_())


class Asteria(QMainWindow):

    def __init__(self, name: str, ground: tuple[str, int], port: int):
        super().__init__()

        self.name = name
        self.ground = ground
        self.port = port

        # Create the socket to send commands to the ground.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Create the GUI.
        self.orientation = None
        self.temperature = None
        self.proximity = None
        self.init_ui()

        # Spawn the telemetry thread to receive telemetry.
        self.telemetry_thread = TelemetryThread(port)
        self.telemetry_thread.update_telemetry.connect(self.update_telemetry)
        self.telemetry_thread.start()

    def init_ui(self):
        # Setup.
        self.setWindowTitle(self.name)
        self.setGeometry(100, 100, 400, 300)
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)

        # Telemetry.
        telemetry_layout = QVBoxLayout()
        telemetry_label = QLabel("Telemetry", self)
        telemetry_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.orientation_label = QLabel(f"Orientation (q): -", self)
        self.temperature_label = QLabel(f"Temperature (°F): -", self)
        self.proximity_label = QLabel(f"Proximity (ft): -", self)
        telemetry_layout.addWidget(telemetry_label)
        telemetry_layout.addWidget(self.orientation_label)
        telemetry_layout.addWidget(self.temperature_label)
        telemetry_layout.addWidget(self.proximity_label)
        main_layout.addLayout(telemetry_layout)

        # Command.
        command_layout = QVBoxLayout()
        command_label = QLabel("Command", self)
        command_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        button_layout = QHBoxLayout()
        minimum_button = QPushButton("Minimum", self)
        minimum_button.clicked.connect(lambda _: self.send_command(b"\x00"))
        center_button = QPushButton("Center", self)
        center_button.clicked.connect(lambda _: self.send_command(b"\x01"))
        maximum_button = QPushButton("Maximum", self)
        maximum_button.clicked.connect(lambda _: self.send_command(b"\x02"))
        button_layout.addWidget(minimum_button)
        button_layout.addWidget(center_button)
        button_layout.addWidget(maximum_button)
        command_layout.addWidget(command_label)
        command_layout.addLayout(button_layout)
        main_layout.addLayout(command_layout)

        # Visualization.
        visualization_layout = QVBoxLayout()
        visualization_label = QLabel("Visualization", self)
        visualization_label.setStyleSheet(
            "font-weight: bold; font-size: 16px;")
        visualization_layout.addWidget(visualization_label)
        open_button = QPushButton("Open Visualization", self)
        open_button.clicked.connect(self.open_visualization_window)
        visualization_layout.addWidget(open_button)
        main_layout.addLayout(visualization_layout)

        main_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Info.
        info_layout = QHBoxLayout()
        connected_label = QLabel(
            f"Connected to ground station @ {self.ground[0]}:{self.ground[1]}")
        connected_label.setStyleSheet(
            "color: green; font-weight: bold; font-size: 10px;")
        info_layout.addWidget(connected_label)
        main_layout.addLayout(info_layout)

        # Finalize.
        self.setCentralWidget(central_widget)

    def open_visualization_window(self):
        self.visualization_window = VisualizationWindow()
        self.visualization_window.show()

    def send_command(self, command: bytes):
        self.socket.sendto(command, self.ground)
        logger.info(f"Sent {command=} to ground.")

    def update_telemetry(self, telemetry: bytes):
        telemetry = telemetry[0]
        self.orientation = (fixed_bytes_to_float(telemetry[0:4], 0.0, 1.00),
                            fixed_bytes_to_float(telemetry[4:8], 0.0, 1.00),
                            fixed_bytes_to_float(telemetry[8:12], 0.0, 1.00),
                            fixed_bytes_to_float(telemetry[12:16], 0.0, 1.00))
        self.proximity = fixed_bytes_to_float(telemetry[16:20], 0.0, 1000.0)
        self.temperature = fixed_bytes_to_float(telemetry[20:24], -100, 100)
        self.proximity *= 0.0328084
        self.temperature = self.temperature * 9 / 5 + 32
        self.orientation_label.setText(
            "Orientation (q): ({:.3f}, {:.3f}, {:.3f}, {:.3f})".format(
                *self.orientation))
        self.temperature_label.setText(
            f"Temperature (°F): {self.temperature:.3f}")
        self.proximity_label.setText(f"Proximity (ft): {self.proximity:.3f}")

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
            self.update_telemetry.emit((telemetry, ))
