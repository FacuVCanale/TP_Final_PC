import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from communication.client.client import MountainClient
import itertools

client = MountainClient('localhost', 8080)

# Crear la figura y el gráfico 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Inicializar el gráfico de dispersión
scatter = None  # Variable global
points = []  # Lista para almacenar los puntos

# Función para actualizar el gráfico en cada iteración
def update_graph(frame):
    global scatter  # Usar la variable global
    global points  # Usar la variable global

    # Obtener los datos del cliente
    info = client.get_data()

    # Recorrer los datos y extraer las coordenadas
    for team, climbers in info.items():
        for climber, data in climbers.items():
            x = data['x']
            y = data['y']
            z = data['z']

            # Agregar el punto a la lista
            points.append((x, y, z))

    # Actualizar el gráfico de dispersión con los puntos
    if scatter is not None:
        scatter.remove()

    scatter = ax.scatter(*zip(*points))

    return scatter,

# Crear la animación
ani = FuncAnimation(fig, update_graph, frames=itertools.count(), interval=1000)  # Intervalo en milisegundos

# Configurar los límites del gráfico
ax.set_xlim3d(0, 20000)
ax.set_ylim3d(0, 20000)
ax.set_zlim3d(0, 5000)

# Mostrar el gráfico
plt.show()
