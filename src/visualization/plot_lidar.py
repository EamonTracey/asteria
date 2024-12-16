import matplotlib.pyplot as plt

# Function to read LIDAR data from a file
def read_lidar_data(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    lidar_readings = []
    for line in data:
        if line.strip():  # Skip empty lines
            try:
                # Extract the first value (assuming tuples or single values)
                distance = float(line.strip().strip('()').split(',')[0])
                lidar_readings.append(distance)
            except ValueError:
                print(f"Skipping invalid line: {line}")
    return lidar_readings

# Function to plot LIDAR data
def plot_lidar_data(lidar_readings):
    time = list(range(len(lidar_readings)))  # Time index for x-axis
    plt.figure(figsize=(10, 6))
    plt.plot(time, lidar_readings, color='green', linewidth=2, marker='o', markersize=3, label='LIDAR Distance')
    plt.title('LIDAR Distance Readings Over Time')
    plt.xlabel('Time Index')
    plt.ylabel('Distance (m or relevant unit)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Main function
def main():
    file_path = 'C:/Users/Owner/Documents/CPEG/Code/asteria/LIDARDATA.txt'  # Replace with the actual LIDARDATA file path
    lidar_readings = read_lidar_data(file_path)
    if lidar_readings:
        print(f"Loaded {len(lidar_readings)} LIDAR readings.")
        plot_lidar_data(lidar_readings)
    else:
        print("No valid LIDAR data found in the file.")

# Run the script
if __name__ == "__main__":
    main()
