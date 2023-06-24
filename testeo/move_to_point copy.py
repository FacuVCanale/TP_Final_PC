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


def escalar_montania(x, y, z, dZ_dx, dZ_dy, learning_rate=0.1, momentum=0.9, num_iterations=100):
    v_x, v_y = 0, 0
    
    for i in range(num_iterations):
        # Calcular la velocidad actual con momentum
        v_x = momentum * v_x + learning_rate * dZ_dx
        v_y = momentum * v_y + learning_rate * dZ_dy

        # Actualizar la posición actual utilizando la velocidad
        x -= v_x
        y -= v_y

        dZ_dx, dZ_dy = dxdy(x, y)

        z = -function(x, y)
    # Graficar
        ax.plot_surface(X, Y, Z, cmap="viridis")
        ax.scatter(x, y, z, color="magenta", zorder=1)
        plt.pause(0.01)
        ax.clear()


escalar_montania(70, 70, -function(70,70),-dxdy(70,70)[0], -dxdy(70,70)[1])