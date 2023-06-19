
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from communication.client.client import MountainClient


res = 50

# Crear el rango de valores para los ejes x e y
x = np.linspace(-23000, 23000, res)
y = np.linspace(-23000, 23000, res)

# Crear el meshgrid inicial a partir de los valores de x e y
X, Y = np.meshgrid(x, y)

# Crear la figura y el eje 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

cliente = MountainClient("localhost", 8080)
info = cliente.get_data()

# Crear una matriz Z para almacenar los valores de altura
Z = np.zeros_like(X)

# Funcion de inicializacion
def init():
    return ax,

# Funcion de actualizacion 
def update(frame):
    global X, Y, Z

    # Obtener los datos actualizados del cliente
    info = cliente.get_data()

    # Actualizar los valores de Z en la superficie
    for team, climbers in info.items():
        for climber, data in climbers.items():
            x2 = data['x']
            y2 = data['y']
            z2 = data['z']
            
            # Calcular las distancias entre los puntos (x, y) y (x2, y2) -> EUCLIDEAN
            # Encontrar la posición del punto mAs cercano

            idx_x = np.argmin(abs(x - x2))
            idx_y = np.argmin(abs(y- y2))

            # Obtener las coordenadas (i, j) correspondientes al punto mas cercano
            #i, j = np.unravel_index(closest_index, X.shape) #ESTOY AGARRANDO EL INDEX DE LA POSICION DEL JUGADOR MAS CERCANA AL DE LA MTRIZ CREADA O SEA DEL MESHGRID

            # Asignar el valor de altura al punto correspondiente en Z
            Z[idx_x, idx_y] = z2

    ax.clear()  # Limpiar el eje antes de agregar la nueva superficie
    ax.plot_surface(X, Y, Z, cmap='coolwarm', linewidth=0)

    return ax,

# Animacion
animation = FuncAnimation(fig, update, frames=None, init_func=init, blit=False)

# Mostrar el grafico
plt.show()
