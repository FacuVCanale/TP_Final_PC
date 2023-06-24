import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt

def mishra_bird_function_creator(base_radius):
    def mishra_bird_function(x: float, y: float) -> float:
        x = x / base_radius * 5
        y = y / base_radius * 5
        x = x - 5
        y = y - 5
        f = np.sin(y) * np.exp((1-np.cos(x))**2) + np.cos(x) * np.exp((1-np.sin(y))**2) + (x-y)**2 - 100
        return -f
    return mishra_bird_function

def mishra_bird_gradient_function_creator(base_radius):
    def mishra_bird_function_gradient(x: float, y: float) -> Tuple[float, float]:
        x = x / base_radius * 5
        y = y / base_radius * 5
        x = x - 5
        y = y - 5
        dfdx = 2*(x-y) + np.sin(y) * np.exp((1-np.cos(x))**2) * 2 * (1-np.cos(x)) * np.sin(x) - np.sin(x) * np.exp((1-np.sin(y))**2)
        dfdy = 2*(y-x) - np.cos(x) * np.exp((1-np.sin(y))**2) * 2 * (1-np.sin(y)) * np.cos(y) + np.cos(y) * np.exp((1-np.cos(x))**2)
        return -dfdx, -dfdy   # GRADIENT VECTOR
    return mishra_bird_function_gradient

function = mishra_bird_function_creator(115)
dxdy = mishra_bird_gradient_function_creator(115)

current_pos = [70, 70, -function(70,70), -dxdy(70,70)[0], -dxdy(70,70)[1]]
momentum_x = 0 
momentum_y = 0

alpha = 0.01 #learning rate
beta = 0.5 #momentum

X = np.arange(-115, 115, 1)
Y = np.arange(-115, 115, 1)

X, Y = np.meshgrid(X, Y)

Z = function(X, Y)

ax = plt.subplot(projection="3d", computed_zorder=False)

for _ in range(100):
    momentum_x = beta * momentum_x + current_pos[3]
    momentum_y = beta * momentum_y + current_pos[4]

    x_new, y_new = current_pos[0] - alpha * momentum_x, current_pos[1] - alpha * momentum_y

    dx, dy = dxdy(x_new, y_new)
    current_pos = (x_new, y_new, -function(x_new, y_new), -dx, -dy)

    ax.plot_surface(X, Y, Z, cmap="viridis")
    ax.scatter(current_pos[0], current_pos[1], -current_pos[2], color="magenta", zorder=1)
    plt.pause(0.01)
    ax.clear()

