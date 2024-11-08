import tkinter as tk
from PIL import Image, ImageTk
import socket
import threading
import struct
from io import BytesIO
import random
import numpy as np
import trimesh
from pythreejs import Mesh, BufferGeometry, MeshStandardMaterial, PerspectiveCamera, Scene, AmbientLight, DirectionalLight, SpotLight, OrbitControls, Renderer, Matrix4
import time
import os

# Setup Tkinter window
root = tk.Tk()
root.title("ASTERIA Monitoring")
root.geometry("900x1000")
root.configure(bg="#f0f0f0")

# Title label
title_label = tk.Label(root, text="ASTERIA Monitoring", font=("Helvetica", 18, "bold"), fg="#003366", bg="#f0f0f0")
title_label.pack(pady=10)

# Health data display (now displaying temperature)
temp_label_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.SOLID)
temp_label_frame.pack(pady=10, padx=20, fill=tk.X)
temp_label_title = tk.Label(temp_label_frame, text="Temperature: ", font=("Helvetica", 14, "bold"), anchor="w", bg="#ffffff")
temp_label_title.pack(side=tk.LEFT, padx=10)
temp_label = tk.Label(temp_label_frame, text="Unknown", font=("Helvetica", 14), fg="#555555", bg="#ffffff")
temp_label.pack(side=tk.LEFT, padx=5)

# Orientation data display
orientation_label_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.SOLID)
orientation_label_frame.pack(pady=10, padx=20, fill=tk.X)
orientation_label_title = tk.Label(orientation_label_frame, text="Orientation: ", font=("Helvetica", 14, "bold"), anchor="w", bg="#ffffff")
orientation_label_title.pack(side=tk.LEFT, padx=10)
orientation_label = tk.Label(orientation_label_frame, text="Unknown", font=("Helvetica", 14), fg="#555555", bg="#ffffff")
orientation_label.pack(side=tk.LEFT, padx=5)

# LiDAR data display
lidar_label_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.SOLID)
lidar_label_frame.pack(pady=10, padx=20, fill=tk.X)
lidar_label_title = tk.Label(lidar_label_frame, text="LiDAR Proximity: ", font=("Helvetica", 14, "bold"), anchor="w", bg="#ffffff")
lidar_label_title.pack(side=tk.LEFT, padx=10)
lidar_label = tk.Label(lidar_label_frame, text="Unknown", font=("Helvetica", 14), fg="#555555", bg="#ffffff")
lidar_label.pack(side=tk.LEFT, padx=5)

# Image display
image_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.SOLID)
image_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
image_label_title = tk.Label(image_frame, text="Camera View: ", font=("Helvetica", 14, "bold"), anchor="w", bg="#ffffff")
image_label_title.pack(pady=5)
image_label = tk.Label(image_frame, bg="#ffffff")
image_label.pack()

# Orientation visualization
orientation_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.SOLID)
orientation_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
orientation_label_title = tk.Label(orientation_frame, text="Orientation Visualizer", font=("Helvetica", 14, "bold"), anchor="w", bg="#ffffff")
orientation_label_title.pack(pady=5)
orientation_canvas = tk.Canvas(orientation_frame, width=400, height=400, bg="#f0f0f0")
orientation_canvas.pack()

# Boolean command function to simulate sending land commands back
def send_command(land_top):
    command = 'TOP' if land_top else 'BOTTOM'
    # For now, simply print the simulated command
    print(f"Simulated Command sent: {command}")

# Buttons for user input
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=20)

top_button = tk.Button(button_frame, text="Land on Top", command=lambda: send_command(True), font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=20, pady=10)
top_button.pack(side=tk.LEFT, padx=20)

bottom_button = tk.Button(button_frame, text="Land on Bottom", command=lambda: send_command(False), font=("Helvetica", 12), bg="#F44336", fg="white", padx=20, pady=10)
bottom_button.pack(side=tk.RIGHT, padx=20)

# Read IMU data from file
def read_imu_data(file_path):
    if not os.path.isabs(file_path):
        file_path = os.path.join(os.path.dirname(__file__), file_path)
    lidar_distance = 100.0
    temperature = 50.0
    with open(file_path, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                f.seek(0)  # Restart reading the file when reaching the end
                continue
            quaternion = [float(x) for x in line.strip('()\n').split(', ')]
            orientation = quaternion_to_euler(quaternion)
            lidar_distance = max(0.0, lidar_distance - 1.0)  # Decrease LiDAR distance from 100m to 0m
            temperature = max(0.0, temperature - 0.5)  # Decrease temperature from 50°C to 0°C
            image_data = None  # No simulated image data for now

            # Update the GUI with the data
            root.after(0, update_gui, temperature, orientation, lidar_distance, image_data)
            time.sleep(1)  # Simulate data coming in every second

def quaternion_to_euler(quaternion):
    w, x, y, z = quaternion
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = np.arctan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = np.arcsin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = np.arctan2(t3, t4)

    return (roll_x, pitch_y, yaw_z)

def update_gui(temperature=None, orientation=None, lidar_distance=None, image_data=None):
    # Update temperature
    temp_label.config(text=f"{temperature:.2f} °C")

    # Update orientation (displaying roll, pitch, and yaw)
    orientation_text = f"Roll: {np.degrees(orientation[0]):.2f}°, Pitch: {np.degrees(orientation[1]):.2f}°, Yaw: {np.degrees(orientation[2]):.2f}°"
    orientation_label.config(text=orientation_text)
    update_orientation_visualization(orientation)

    # Update LiDAR data
    lidar_label.config(text=f"{lidar_distance:.2f} m")

    # Update the image display
    if image_data:
        try:
            img = Image.open(BytesIO(image_data))
            img = img.resize((300, 300))  # Resize for display
            img = ImageTk.PhotoImage(img)
            image_label.config(image=img)
            image_label.image = img
        except Exception as e:
            print("Error loading image:", e)

def update_orientation_visualization(orientation):
    # Placeholder: Update orientation visualization in the orientation_canvas
    # Here, we'll draw an arrow to indicate the change in orientation
    orientation_canvas.delete("all")
    x, y, z = orientation
    center_x, center_y = 200, 200
    scale = 100

    # Calculate the end point of the arrow based on orientation values
    end_x = center_x + scale * np.cos(y) * np.cos(z)
    end_y = center_y - scale * np.sin(y)

    # Draw the arrow representing the orientation
    orientation_canvas.create_line(center_x, center_y, end_x, end_y, arrow=tk.LAST, fill="blue", width=3)

# Start reading IMU data from REALIMUDATA.txt in a separate thread to avoid blocking the GUI
data_thread = threading.Thread(target=read_imu_data, args=("../../REALIMUDATA",), daemon=True)
data_thread.start()

# Run the Tkinter GUI
root.mainloop()
