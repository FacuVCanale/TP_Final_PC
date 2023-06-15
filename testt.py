"""DO NOT MODIFY THIS FILE"""
import random
import math
from typing import Tuple

from communication.server.mountain.circularbase_mountain import CircularBaseMountain

class MishraBirdMountain(CircularBaseMountain):
    """Fairly complex mountain modeled after the Mishra's Bird function. The most difficult mountain out of the three 
    examples.
    Args:
        visual_radius (float): the radius of the visual area. If the hiker is at least this far from the flag, it will
            be considered that he has reached the flag.
        base_radius (float): the radius of the base of the mountain. If the hiker goes outside this radius, he will be
            considered out of bounds and disqualified.
    """
    def __init__(self, visual_radius: float, base_radius: float) -> None:
        super().__init__(mishra_bird_function_creator(base_radius), mishra_bird_gradient_function_creator(base_radius), None, visual_radius, base_radius)
        self.generate_random_flag(base_radius)

    def generate_random_flag(self, base_radius: float) -> None:
        flag = [random.uniform(-10, 10), random.uniform(-10, 10)]
        flag[0] = flag[0] * base_radius / 5
        flag[1] = flag[1] * base_radius / 5
        flag[0] = flag[0] - 5
        flag[1] = flag[1] - 5
        self.flag = tuple(flag)


def mishra_bird_function_creator(base_radius):
    def mishra_bird_function(x: float, y: float) -> float:
        x = x / base_radius * 5
        y = y / base_radius * 5
        x = x - 5
        y = y - 5
        f = math.sin(y) * math.exp((1-math.cos(x))**2) + math.cos(x) * math.exp((1-math.sin(y))**2) + (x-y)**2 - 100
        return -f
    return mishra_bird_function

def mishra_bird_gradient_function_creator(base_radius):
    def mishra_bird_function_gradient(x: float, y: float) -> Tuple[float, float]:
        x = x / base_radius * 5
        y = y / base_radius * 5
        x = x - 5
        y = y - 5
        dfdx = 2*(x-y) + math.sin(y) * math.exp((1-math.cos(x))**2) * 2 * (1-math.cos(x)) * math.sin(x) - math.sin(x) * math.exp((1-math.sin(y))**2)
        dfdy = 2*(y-x) - math.cos(x) * math.exp((1-math.sin(y))**2) * 2 * (1-math.sin(y)) * math.cos(y) + math.cos(y) * math.exp((1-math.cos(x))**2)
        return -dfdx, -dfdy
    return mishra_bird_function_gradient

import matplotlib.pyplot as plt
import numpy as np

# Define the range of x and y values
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)

# Create a grid of x and y values
X, Y = np.meshgrid(x, y)

# Create an instance of the MishraBirdMountain class
mountain = MishraBirdMountain(visual_radius=10, base_radius=10)
mishra_bird_function = mishra_bird_function_creator(mountain.base_radius)

# Calculate the function values for each point in the grid
Z = np.zeros_like(X)
for i in range(len(x)):
    for j in range(len(y)):
        Z[i, j] = mishra_bird_function(X[i, j], Y[i, j])

# Create a contour plot
plt.figure(figsize=(8, 6))
plt.contourf(X, Y, Z, levels=50, cmap='viridis')
plt.colorbar()

# Set labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title("Mishra's Bird Mountain")

# Show the plot
plt.show()

