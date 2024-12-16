import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Function to read LIDAR data
def read_lidar_data(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return [float(line.strip().strip('()').split(',')[0]) for line in data if line.strip()]

# Function to plot LIDAR data
def plot_lidar_data(lidar_readings):
    time = list(range(len(lidar_readings)))
    plt.figure(figsize=(8, 5))
    plt.plot(time, lidar_readings, color='green', linewidth=2, marker='o', markersize=3, label='LIDAR Distance')
    plt.title('LIDAR Distance Readings Over Time')
    plt.xlabel('Time Index')
    plt.ylabel('Distance (m or relevant unit)')
    plt.grid(True)
    plt.legend()

# Function to read orientation data
def read_orientation_data(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return [tuple(map(float, line.strip().strip('()').split(','))) for line in data if line.strip()]

# Function to plot quaternion data
def plot_quaternion(quaternions):
    time = list(range(len(quaternions)))
    x = [q[0] for q in quaternions]
    y = [q[1] for q in quaternions]
    z = [q[2] for q in quaternions]
    w = [q[3] for q in quaternions]
    
    plt.figure(figsize=(8, 5))
    plt.plot(time, x, label='x', linewidth=2)
    plt.plot(time, y, label='y', linewidth=2)
    plt.plot(time, z, label='z', linewidth=2)
    plt.plot(time, w, label='w', linewidth=2)
    plt.title('Quaternion Components Over Time')
    plt.xlabel('Time Index')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)

# Function to read temperature data
def read_temperature_data(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return [float(line.strip().strip('()').split(',')[0]) for line in data if line.strip()]

# Function to plot temperature data
def plot_temperature(temperatures):
    time = list(range(len(temperatures)))
    plt.figure(figsize=(8, 5))
    plt.plot(time, temperatures, color='orange', linewidth=2, marker='o', markersize=3, label='Temperature')
    plt.title('Temperature Data Over Time')
    plt.xlabel('Time Index')
    plt.ylabel('Temperature (°C or relevant unit)')
    plt.grid(True)
    plt.legend()

# Main function to save all plots into a PDF
import datetime  # Add this at the top

def main():
    lidar_file = 'C:/Users/Owner/Documents/CPEG/Code/asteria/LIDARDATA.txt'
    imu_file = 'C:/Users/Owner/Documents/CPEG/Code/asteria/REALIMUDATA.txt'
    temp_file = 'C:/Users/Owner/Documents/CPEG/Code/asteria/TEMPDATA.txt'

    # Create a single PDF to save all plots
    with PdfPages('output_plots.pdf') as pdf:
        # Plot LIDAR data
        lidar_readings = read_lidar_data(lidar_file)
        if lidar_readings:
            plot_lidar_data(lidar_readings)
            pdf.savefig()  # Save current figure to PDF
            plt.close()
        
        # Plot Quaternion data
        quaternions = read_orientation_data(imu_file)
        if quaternions:
            plot_quaternion(quaternions)
            pdf.savefig()  # Save current figure to PDF
            plt.close()
        
        # Plot Temperature data
        temperatures = read_temperature_data(temp_file)
        if temperatures:
            plot_temperature(temperatures)
            pdf.savefig()  # Save current figure to PDF
            plt.close()
        
        # Add metadata to PDF
        d = pdf.infodict()
        d['Title'] = 'Sensor Data Plots'
        d['Author'] = 'Your Name'
        d['Subject'] = 'Combined Plots for LIDAR, IMU, and Temperature Data'
        d['Keywords'] = 'LIDAR, Quaternion, Temperature, Plots'
        d['CreationDate'] = datetime.datetime.today()

    print("All plots have been saved to 'output_plots.pdf'.")


if __name__ == "__main__":
    main()
