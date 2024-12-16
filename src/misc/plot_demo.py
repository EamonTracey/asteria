import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import os
import numpy as np
import re
import math


def quaternion_to_euler(w, x, y, z):
    magnitude = math.sqrt(w**2 + x**2 + y**2 + z**2)
    w, x, y, z = w / magnitude, x / magnitude, y / magnitude, z / magnitude
    sin_pitch = 2.0 * (w * y - z * x)

    if abs(sin_pitch) >= 1:
        pitch = math.copysign(math.pi / 2, sin_pitch)
        roll = 0
        yaw = math.atan2(2 * (w * z + x * y), 1 - 2 * (y**2 + z**2))
    else:
        pitch = math.asin(sin_pitch)
        roll = math.atan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x**2 + y**2))
        yaw = math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y**2 + z**2))

    return math.degrees(roll), math.degrees(pitch), math.degrees(yaw)


def smooth_data(data, window_size=10):
    return np.convolve(data, np.ones(window_size) / window_size, mode="same")


def plot_quaternion(data):
    time = data["Time"]
    w = smooth_data(data["Quaternion_W_BNO085"])
    x = smooth_data(data["Quaternion_X_BNO085"])
    y = smooth_data(data["Quaternion_Y_BNO085"])
    z = smooth_data(data["Quaternion_Z_BNO085"])

    plt.figure(figsize=(8, 5))
    plt.plot(time, w, label="w", linewidth=2)
    plt.plot(time, x, label="x", linewidth=2)
    plt.plot(time, y, label="y", linewidth=2)
    plt.plot(time, z, label="z", linewidth=2)
    plt.title("IMU Fusion Quaternions (Orientation)")
    plt.xlabel("Time (s)")
    plt.ylabel("Orientation (q)")
    plt.legend()
    plt.grid(True)


def plot_euler(data):
    time = data["Time"]
    qw = smooth_data(data["Quaternion_W_BNO085"])
    qx = smooth_data(data["Quaternion_X_BNO085"])
    qy = smooth_data(data["Quaternion_Y_BNO085"])
    qz = smooth_data(data["Quaternion_Z_BNO085"])

    eulers = [
        quaternion_to_euler(w, x, y, z)
        for (w, x, y, z) in zip(qw, qx, qy, qz)
    ]
    rolls = [euler[0] for euler in eulers]
    pitches = [euler[1] for euler in eulers]
    yaws = [euler[2] for euler in eulers]

    plt.figure(figsize=(8, 5))
    plt.plot(time, rolls, label="Roll", linewidth=2)
    plt.plot(time, pitches, label="Pitch", linewidth=2)
    plt.plot(time, yaws, label="Yaw", linewidth=2)
    plt.title("IMU Fusion Euler Angles (Orientation)")
    plt.xlabel("Time (s)")
    plt.ylabel("Orientation (degrees)")
    plt.legend()
    plt.grid(True)


def plot_lidar(data):
    time = data["Time"]
    proximity = smooth_data(data["Proximity_Lidar"] * 0.0328084)
    stages = data["Stage"]

    stage_change_indices = []
    stage_values = []
    previous_stage = None

    for i, stage in enumerate(stages):
        if stage != previous_stage:
            stage_change_indices.append(i)
            stage_values.append(proximity[i])
            previous_stage = stage

    plt.figure(figsize=(8, 5))
    plt.plot(time, proximity, color="green", linewidth=2, label="Proximity")

    plt.scatter([time[i] for i in stage_change_indices],
                stage_values,
                color="red",
                marker="o",
                s=100,
                label="Stage Change")

    plt.title("LiDaR Proximity w/ Stage Markers")
    plt.xlabel("Time (s)")
    plt.ylabel("Proximity (ft)")
    plt.legend()
    plt.grid(True)


def plot_temperature(data):
    time = data["Time"]
    temperature = smooth_data(data["Temperature_MCP9808"] * (9 / 5) + 32)

    plt.figure(figsize=(8, 5))
    plt.plot(time, temperature, color="orange", linewidth=2)
    plt.title("Temperature")
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (°F)")
    plt.ylim(70, 90)
    plt.grid(True)


def add_images_to_pdf(image_folder, pdf):
    images = os.listdir(image_folder)
    images = [
        image for image in images if image.lower().endswith((".jpg", ".jpeg"))
    ]
    images = sorted(images, key=lambda q: int(re.search(r"\d+", q).group()))
    for filename in images:
        img_path = os.path.join(image_folder, filename)
        image = Image.open(img_path)

        plt.figure(figsize=(8, 5))
        plt.imshow(image)
        plt.axis("off")
        plt.title(f"Image: {filename}")
        pdf.savefig()
        plt.close()
        print(f"Added {filename} to the PDF.")


def plot_acceleration(data):
    time = data["Time"]
    ax = data["Acceleration_X_BNO085"]
    ay = data["Acceleration_Y_BNO085"]
    az = data["Acceleration_Z_BNO085"]

    times = np.array(time)
    aax = smooth_data(np.gradient(np.array(ax), times))
    aay = smooth_data(np.gradient(np.array(ay), times))
    aaz = smooth_data(np.gradient(np.array(az), times))

    plt.figure(figsize=(8, 5))
    plt.plot(time, aax, label="X", linewidth=2)
    plt.plot(time, aay, label="Y", linewidth=2)
    plt.plot(time, aaz, label="Z", linewidth=2)
    plt.title("Acceleration")
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s²)")
    plt.legend()
    plt.grid(True)


def main():
    data = pd.read_csv("demo/demo.csv")
    print(f"Loaded data with {len(data)} records and {data.shape[1]} columns.")

    pdf_filename = "demo.pdf"
    with PdfPages(pdf_filename) as pdf:
        # Plot orientation.
        plot_quaternion(data)
        pdf.savefig()
        plt.close()

        # Plot orientation.
        plot_euler(data)
        pdf.savefig()
        plt.close()

        # Plot acceleration.
        plot_acceleration(data)
        pdf.savefig()
        plt.close()

        # Plot LiDaR.
        plot_lidar(data)
        pdf.savefig()
        plt.close()

        # Plot temperature.
        plot_temperature(data)
        pdf.savefig()
        plt.close()

        # Add images.
        add_images_to_pdf("demo", pdf)

        # PDF metadata.
        d = pdf.infodict()
        d["Title"] = "Asteria Sensor Log Data with Images"
        d["Author"] = "Team 3"
        d["Subject"] = "Visualization of Quaternion, LIDAR, Temperature Data, and Images"
        d["Keywords"] = "Sensor Data, Quaternion, LIDAR, Temperature, Images"
        d["CreationDate"] = pd.Timestamp.now()

    print(f"All plots and images have been saved to \"{pdf_filename}\".")


if __name__ == "__main__":
    main()
