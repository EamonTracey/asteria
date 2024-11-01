import pythreejs as three
import json
import os
import ipywidgets
import ipywidgets.embed as embed
from IPython.display import display
from ipywidgets import VBox
import socket
import threading
import numpy as np
from pythreejs import Mesh, BufferGeometry, MeshStandardMaterial, PerspectiveCamera, Scene, AmbientLight, DirectionalLight, OrbitControls, Renderer, Matrix4
import trimesh
from trimesh.exchange import gltf


class LanderVisualization:

    def __init__(self, model_path):
        # Set up the scene.
        self.scene = Scene(children=[AmbientLight(color='#ffffff')])

        # Set up the camera.
        self.camera = PerspectiveCamera(position=[10, 10, 10],
                                        children=[
                                            DirectionalLight(
                                                color='white',
                                                position=[3, 5, 1],
                                                intensity=0.6)
                                        ])

        # Set up controls.
        self.controls = OrbitControls(controlling=self.camera)

        # Set up renderer.
        self.renderer = Renderer(scene=self.scene,
                                 camera=self.camera,
                                 controls=[self.controls],
                                 antialias=True,
                                 alpha=True,
                                 width=800,
                                 height=600)

        # Load the model.
        self.load_model(model_path)

        # Set up threading for receiving IMU data
        self.stop_thread = False
        self.thread = threading.Thread(target=self.receive_imu_data)
        self.thread.start()

    def load_model(self, model_path):
        """Loads a GLB model using trimesh and adds it to the scene."""
        mesh = trimesh.load(model_path, force='mesh')

        # Ensure the vertices and faces are properly formatted
        vertices = mesh.vertices.astype(
            np.float32)  # Convert vertices to float32 if not already
        faces = mesh.faces.flatten().astype(
            np.uint32)  # Convert faces to unsigned 32-bit integer

        geometry = BufferGeometry(
            attributes={
                'position': three.BufferAttribute(vertices, normalized=False),
                'index': three.BufferAttribute(faces, normalized=False)
            })

        # Use a valid HTML color for the material
        material = MeshStandardMaterial(
            color='#808080')  # You could also use 'gray' (U.S. spelling)
        self.model = Mesh(geometry, material)
        self.scene.add(self.model)

    def display(self):
        """Displays the 3D model in a Jupyter notebook."""
        display(self.renderer)

    def save_html(self, file_name):
        """Saves the current visualization as an HTML file."""
        box = VBox([self.renderer])
        with open(file_name, 'w') as f:
            embed.embed_minimal_html(f,
                                     views=[box],
                                     title='Lander Visualization')

    def receive_imu_data(self):
        """Receives IMU data over a socket and updates the model's orientation."""
        # Set up a socket to receive IMU data
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', 5005))  # Listening on port 5005

        while not self.stop_thread:
            try:
                data, _ = sock.recvfrom(1024)
                imu_data = json.loads(data.decode('utf-8'))
                quaternion = imu_data.get('quaternion', [1, 0, 0, 0])
                self.update_orientation(quaternion)
            except Exception as e:
                print(f"Error receiving IMU data: {e}")
                continue

    def update_orientation(self, quaternion):
        """Updates the orientation of the model based on the received quaternion."""
        if hasattr(self, 'model'):
            q = np.array(quaternion)
            # Convert quaternion to a rotation matrix
            rot_matrix = self.quaternion_to_rotation_matrix(q)
            self.model.matrix = Matrix4(elements=rot_matrix.flatten().tolist())
            self.model.matrixAutoUpdate = False

    @staticmethod
    def quaternion_to_rotation_matrix(q):
        """Converts a quaternion into a 4x4 rotation matrix."""
        qw, qx, qy, qz = q
        rot_matrix = np.array([[
            1 - 2 * qy**2 - 2 * qz**2, 2 * qx * qy - 2 * qz * qw,
            2 * qx * qz + 2 * qy * qw, 0
        ],
                               [
                                   2 * qx * qy + 2 * qz * qw,
                                   1 - 2 * qx**2 - 2 * qz**2,
                                   2 * qy * qz - 2 * qx * qw, 0
                               ],
                               [
                                   2 * qx * qz - 2 * qy * qw,
                                   2 * qy * qz + 2 * qx * qw,
                                   1 - 2 * qx**2 - 2 * qy**2, 0
                               ], [0, 0, 0, 1]])
        return rot_matrix

    def close(self):
        """Stops the thread and closes resources."""
        self.stop_thread = True
        self.thread.join()


# Example usage
if __name__ == "__main__":
    print("Hi, I'm the lander visualization!")
    model_path = "C:/Users/Owner/Documents/CPEG/Code/asteria/cad/Asteria_Inside_Body.glb"
    if not os.path.exists(model_path):
        print(f"Error: File not found at {model_path}")
    else:
        viz = LanderVisualization(model_path)
        viz.display()
