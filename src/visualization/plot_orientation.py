import matplotlib.pyplot as plt

# Function to read the orientation data from a file
def read_orientation_data(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    quaternions = []
    for line in data:
        if line.strip():
            # Convert the string tuple to a list of floats
            quaternions.append(tuple(map(float, line.strip().strip('()').split(','))))
    return quaternions

# Function to plot the quaternion components
def plot_quaternion(quaternions):
    # Extract the individual components
    time = list(range(len(quaternions)))  # Assuming sequential time indices
    x = [q[0] for q in quaternions]
    y = [q[1] for q in quaternions]
    z = [q[2] for q in quaternions]
    w = [q[3] for q in quaternions]
    
    # Plot each component
    plt.figure(figsize=(10, 6))
    plt.plot(time, x, label='x', linewidth=2)
    plt.plot(time, y, label='y', linewidth=2)
    plt.plot(time, z, label='z', linewidth=2)
    plt.plot(time, w, label='w', linewidth=2)
    plt.title('Quaternion Components Over Time')
    plt.xlabel('Time Index')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Main function
def main():
    file_path = 'C:/Users/Owner/Documents/CPEG/Code/asteria/REALIMUDATA.txt'  # Replace with the path to your file
    quaternions = read_orientation_data(file_path)
    plot_quaternion(quaternions)

# Run the script
if __name__ == "__main__":
    main()
