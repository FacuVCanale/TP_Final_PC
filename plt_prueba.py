import matplotlib.pyplot as plt
import numpy as np

# Define the player coordinates
facu = [1, 2, 3]  # [x, y, z]
fran = [2, 3, 4]
luqui = [3, 4, 5]
cami = [4, 5, 6]

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Generate a grid of x, y values
x = np.linspace(0, 5, 10)
y = np.linspace(0, 5, 10)
X, Y = np.meshgrid(x, y)

# Generate a dummy Z values for the surface plot
Z = np.zeros_like(X)

# Plot the surface
ax.plot_surface(X, Y, Z, cmap="viridis")

# Plot the player positions
ax.scatter(facu[0], facu[1], -facu[2], color="magenta", zorder=1)
ax.scatter(fran[0], fran[1], -fran[2], color="red", zorder=2)
ax.scatter(luqui[0], luqui[1], -luqui[2], color="blue", zorder=3)
ax.scatter(cami[0], cami[1], -cami[2], color="green", zorder=4)

# Show the plot
plt.show()
