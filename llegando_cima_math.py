import numpy as np
import matplotlib.pyplot as plt

def find_higher_z(points):
    # Convert the list of lists to a NumPy array for easier manipulation
    data = np.array(points)

    # Extract the x, y, and z values from the data
    x_values = data[:, 0]
    y_values = data[:, 1]
    z_values = data[:, 2]

    # Calculate the maximum z value and its index
    max_z_index = np.argmax(z_values)
    max_z = z_values[max_z_index]

    # Calculate the differences between the maximum z value and other z values
    z_diffs = max_z - z_values

    # Calculate the new x and y values to reach a higher z value
    new_x = x_values[max_z_index] + z_diffs[max_z_index] * data[max_z_index, 3]
    new_y = y_values[max_z_index] + z_diffs[max_z_index] * data[max_z_index, 4]

    return new_x, new_y

# Example usage
points = [[1, 2, 5, 0.1, 0.2], [3, 4, 7, 0.3, 0.4], [5, 6, 9, 0.5, 0.6]]
new_x, new_y = find_higher_z(points)
print("New x:", new_x)
print("New y:", new_y)

x = [i[0] for i in points]
y = [i[1] for i in points]
z = [i[2] for i in points]

plt.scatter(x,y, c=z)
plt.colorbar()
plt.show()