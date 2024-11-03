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
from pythreejs import Mesh, BufferGeometry, MeshStandardMaterial, PerspectiveCamera, Scene, AmbientLight, DirectionalLight, SpotLight, OrbitControls, Renderer, Matrix4
import trimesh
from trimesh.exchange import gltf
import time


class LanderVisualization:

    def __init__(self, model_paths):
        # Set up the scenes for inside and outside models.
        self.inside_scene = Scene(
            children=[AmbientLight(color='#ffffff', intensity=0.5)])
        self.outside_scene = Scene(
            children=[AmbientLight(color='#ffffff', intensity=0.5)])

        # Add additional lighting for better visualization.
        spotlight_inside = SpotLight(color='white',
                                     intensity=1.0,
                                     position=[15, 15, 15],
                                     angle=0.3,
                                     penumbra=0.2)
        spotlight_outside = SpotLight(color='white',
                                      intensity=1.0,
                                      position=[15, 15, 15],
                                      angle=0.3,
                                      penumbra=0.2)
        self.inside_scene.add(spotlight_inside)
        self.outside_scene.add(spotlight_outside)

        # Set up the camera for both scenes.
        self.camera = PerspectiveCamera(position=[10, 10, 10],
                                        children=[
                                            DirectionalLight(
                                                color='white',
                                                position=[3, 5, 1],
                                                intensity=0.6)
                                        ])

        # Set up orbit controls for the camera to allow user interaction.
        self.controls = OrbitControls(controlling=self.camera)

        # Set up renderers for both scenes.
        self.inside_renderer = Renderer(scene=self.inside_scene,
                                        camera=self.camera,
                                        controls=[self.controls],
                                        antialias=True,
                                        alpha=True,
                                        width=400,
                                        height=600)

        self.outside_renderer = Renderer(scene=self.outside_scene,
                                         camera=self.camera,
                                         controls=[self.controls],
                                         antialias=True,
                                         alpha=True,
                                         width=400,
                                         height=600)

        # Load the models into their respective scenes.
        self.load_model(model_paths[0], self.inside_scene)
        self.load_model(model_paths[1], self.outside_scene)

        # Set up threading for receiving IMU data or simulating IMU data.
        self.stop_thread = False
        self.thread = threading.Thread(target=self.simulate_imu_data)
        self.thread.start()

    def load_model(self, model_path, scene):
        """Loads a GLB model using trimesh and adds it to the specified scene."""
        mesh = trimesh.load(model_path, force='mesh')

        # Ensure the vertices and faces are properly formatted.
        vertices = mesh.vertices.astype(
            np.float32)  # Convert vertices to float32 if not already
        faces = mesh.faces.flatten().astype(
            np.uint32)  # Convert faces to unsigned 32-bit integer

        # Create a BufferGeometry object from the loaded mesh data.
        geometry = BufferGeometry(
            attributes={
                'position': three.BufferAttribute(vertices, normalized=False),
                'index': three.BufferAttribute(faces, normalized=False)
            })

        # Create a shiny material with a different color and high metalness for better visualization.
        material = MeshStandardMaterial(
            color='#ffd700', metalness=1.0,
            roughness=0.1)  # Gold color, shiny material
        model = Mesh(geometry, material)

        # Add the mesh to the specified scene.
        scene.add(model)

    def display(self):
        """Displays the 3D models in a Jupyter notebook."""
        display(VBox([self.inside_renderer, self.outside_renderer]))

    def save_html(self, file_name):
        """Saves the current visualization as an HTML file."""
        box = VBox([self.inside_renderer, self.outside_renderer])
        with open(file_name, 'w') as f:
            embed.embed_minimal_html(f,
                                     views=[box],
                                     title='Lander Visualization')

    def simulate_imu_data(self):
        """Simulates IMU data to update the model's orientation."""
        while not self.stop_thread:
            # Generate a simulated quaternion representing rotation around the z-axis.
            angle_z = (
                time.time() % (4 * np.pi)
            ) / 1.8  # Slower rotating angle for a full 360-degree rotation
            if (time.time() % (8 * np.pi)) < (4 * np.pi):
                quaternion_z = [
                    np.cos(angle_z / 2), 0, 0,
                    np.sin(angle_z / 2)
                ]  # Rotate around the z-axis clockwise
            else:
                quaternion_z = [
                    np.cos(angle_z / 2), 0, 0, -np.sin(angle_z / 2)
                ]  # Rotate around the z-axis counter-clockwise

            # Generate a small teetering angle around the x-axis.
            angle_x = 0.1 * np.sin(
                time.time() * 0.5)  # Small oscillation around x-axis
            quaternion_x = [np.cos(angle_x / 2), np.sin(angle_x / 2), 0, 0]

            # Combine the two quaternions (x and z-axis rotations).
            quaternion = self.combine_quaternions(quaternion_x, quaternion_z)

            self.update_orientation(quaternion)
            time.sleep(0.03)  # Update every 30ms for smoother rotation

    def update_orientation(self, quaternion):
        """Updates the orientation of the models based on the received quaternion."""
        q = np.array(quaternion)
        # Convert quaternion to a rotation matrix.
        rot_matrix = self.quaternion_to_rotation_matrix(q)
        matrix_elements = rot_matrix.flatten().tolist()

        # Update both models in the inside and outside scenes.
        if hasattr(self, 'inside_scene') and hasattr(self, 'outside_scene'):
            for obj in self.inside_scene.children + self.outside_scene.children:
                if isinstance(obj, Mesh):
                    obj.set_trait('matrix', tuple(matrix_elements))
                    obj.matrixAutoUpdate = False

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

    @staticmethod
    def combine_quaternions(q1, q2):
        """Combines two quaternions to create a single rotation."""
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
        z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
        return [w, x, y, z]

    def close(self):
        """Stops the thread and closes resources."""
        self.stop_thread = True
        self.thread.join()


# Example usage
if __name__ == "__main__":
    print("Hi, I'm the lander visualization!")
    model_paths = [
        "C:/Users/Owner/Documents/CPEG/Code/asteria/cad/Asteria_Inside_Body.glb",
        "C:/Users/Owner/Documents/CPEG/Code/asteria/cad/Asteria_Outside_Body.glb"
    ]
    for model_path in model_paths:
        if not os.path.exists(model_path):
            print(f"Error: File not found at {model_path}")
    else:
        # Initialize the visualization with the given model paths.
        viz = LanderVisualization(model_paths)
        # Display the visualization in Jupyter Notebook.
        viz.display()
