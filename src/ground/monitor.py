import tkinter as tk
from PIL import Image, ImageTk
import socket
import threading
import struct
from io import BytesIO

# Setup Tkinter window
root = tk.Tk()
root.title("Flying Device Monitoring")

# Health data display (now displaying temperature)
temp_label = tk.Label(root, text="Temperature: Unknown", font=("Arial", 14))
temp_label.pack()

# Orientation data display
orientation_label = tk.Label(root, text="Orientation: Unknown", font=("Arial", 14))
orientation_label.pack()

# Image display
image_label = tk.Label(root)
image_label.pack()

# LiDAR data display
lidar_label = tk.Label(root, text="LiDAR Proximity: Unknown", font=("Arial", 14))
lidar_label.pack()

# Create socket to receive data (matching the command.py setup)
data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data_socket.bind(('0.0.0.0', 12345))  # Make sure to use the correct port

def receive_data():
    while True:
        try:
            # Receiving the data packet
            data, addr = data_socket.recvfrom(4096)  # Adjust buffer size as needed

            # Parse the data packet (assuming struct format)
            temperature, orientation_x, orientation_y, orientation_z, lidar_distance = struct.unpack('f f f f f', data[:20])
            image_data = data[20:]  # Assuming the rest is image data

            # Update the GUI with the new data
            update_gui(temperature, (orientation_x, orientation_y, orientation_z), lidar_distance, image_data)

        except Exception as e:
            print("Error receiving data:", e)

def update_gui(temperature, orientation, lidar_distance, image_data):
    # Update temperature
    temp_label.config(text=f"Temperature: {temperature:.2f} °C")

    # Update orientation (displaying roll, pitch, and yaw)
    orientation_text = f"X: {orientation[0]:.2f}, Y: {orientation[1]:.2f}, Z: {orientation[2]:.2f}"
    orientation_label.config(text=f"Orientation: {orientation_text}")

    # Update LiDAR data
    lidar_label.config(text=f"LiDAR Proximity: {lidar_distance:.2f} m")

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

# Boolean command function to simulate sending land commands back
def send_command(land_top):
    command = 'TOP' if land_top else 'BOTTOM'
    # For now, simply print the simulated command
    print(f"Simulated Command sent: {command}")

# Buttons for user input
top_button = tk.Button(root, text="Land on Top", command=lambda: send_command(True))
top_button.pack(side=tk.LEFT, padx=20)

bottom_button = tk.Button(root, text="Land on Bottom", command=lambda: send_command(False))
bottom_button.pack(side=tk.RIGHT, padx=20)

# Start receiving data in a separate thread to avoid blocking the GUI
data_thread = threading.Thread(target=receive_data, daemon=True)
data_thread.start()

# Run the Tkinter GUI
root.mainloop()
