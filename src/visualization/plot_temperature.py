import matplotlib.pyplot as plt

# Function to read temperature data from a file
def read_temperature_data(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    temperatures = []
    for line in data:
        if line.strip():  # Skip empty lines
            try:
                # Extract single values or tuples
                temp = float(line.strip().strip('()').split(',')[0])
                temperatures.append(temp)
            except ValueError:
                print(f"Skipping invalid line: {line}")
    return temperatures

# Function to plot temperature data
def plot_temperature(temperatures):
    time = list(range(len(temperatures)))  # Time index for x-axis
    plt.figure(figsize=(10, 6))
    plt.plot(time, temperatures, color='orange', linewidth=2, marker='o', markersize=3, label='Temperature')
    plt.title('Temperature Data Over Time')
    plt.xlabel('Time Index')
    plt.ylabel('Temperature (°C or relevant unit)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Main function
def main():
    file_path = 'C:/Users/Owner/Documents/CPEG/Code/asteria/TEMPDATA.txt'  # Replace with your actual TEMPDATA file path
    temperatures = read_temperature_data(file_path)
    if temperatures:
        print(f"Loaded {len(temperatures)} temperature readings.")
        plot_temperature(temperatures)
    else:
        print("No valid temperature data found in the file.")

# Run the script
if __name__ == "__main__":
    main()

