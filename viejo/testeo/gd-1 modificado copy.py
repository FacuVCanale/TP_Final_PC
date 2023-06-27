import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt

def move_to_point_direction(pos_o ,pos_f,vel = 50):
    xo = pos_o[0]
    yo = pos_o[1]
    # zo = pos_o[2]

    xf = pos_f[0]
    yf = pos_f[1]
    # af = pos_f[2]

    v = (xf - xo, yf - yo)
    v_direc = np.arctan(v[0]/v[1])

    return np.degrees(v_direc),vel

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

# current_pos = [70, 70, -function(70,70), -dxdy(70,70)[0], -dxdy(70,70)[1]]
# current_pos = [0, 0, -function(0,0), -dxdy(0,0)[0], -dxdy(0,0)[1]]
current_pos = [40, -100, -function(40,-100), -dxdy(40,-100)[0], -dxdy(40,-100)[1]]

X = np.arange(-115, 115, 1)
Y = np.arange(-115, 115, 1)

X, Y = np.meshgrid(X, Y)

Z = function(X, Y)

ax = plt.subplot(projection="3d", computed_zorder=False)

vel_x = 0 
vel_y = 0

alpha = 0.01 #learning rate
beta = 0.5 #momentum

def apply_gradient_ascent(xo,yo, dx, dy, vel_x=0, vel_y=0, alpha=0.01, beta=0.5,vel=50):
    vel_x = beta * vel_x + alpha * dx
    vel_y = beta * vel_y + alpha * dy

    xf = xo - vel_x
    yf = yo - vel_x

for _ in range(100):
    
    apply_gradient_ascent(current_pos[0],current_pos[1],dxdy(current_pos[0],current_pos[1])[0],dxdy(current_pos[0],current_pos[1])[1])
    
    ax.plot_surface(X, Y, Z, cmap="viridis")
    ax.scatter(current_pos[0], current_pos[1], -current_pos[2], color="magenta", zorder=1)
    plt.pause(0.01)
    ax.clear()

for _ in range(100):
    vel_x = beta * vel_x + alpha * dxdy(current_pos[0],current_pos[1])[0]
    vel_y = beta * vel_x + alpha * dxdy(current_pos[0],current_pos[1])[1]
    x_new, y_new = current_pos[0] +vel_x, current_pos[1] + vel_y

    dx, dy = dxdy(x_new, y_new)
    current_pos = (x_new, y_new, -function(x_new, y_new), -dx, -dy)

    print(x_new, y_new)
    ax.plot_surface(X, Y, Z, cmap="viridis")
    ax.scatter(current_pos[0], current_pos[1], -current_pos[2], color="magenta", zorder=1)
    plt.pause(0.01)
    ax.clear()