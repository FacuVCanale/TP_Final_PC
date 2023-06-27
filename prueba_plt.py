import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Crear una lista vacía para almacenar los puntos
x_values = []
y_values = []

# Crear la figura y los ejes del gráfico
fig, ax = plt.subplots()

# Configurar el gráfico inicialmente
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_title('Gráfico 2D')

# Función para actualizar el gráfico con los nuevos puntos
def update_plot(frame):
    ax.clear()  # Limpiar el gráfico anterior
    ax.scatter(x_values[:frame], y_values[:frame])  # Graficar los puntos actualizados

# Función para agregar puntos al gráfico
def add_point(event):
    if event.inaxes is None:
        return
    x = event.xdata
    y = event.ydata
    x_values.append(x)
    y_values.append(y)
    animation.frame_seq = range(len(x_values))  # Actualizar la secuencia de cuadros de la animación

# Asociar la función add_point al evento 'button_press_event'
fig.canvas.mpl_connect('button_press_event', add_point)

# Crear la animación que llama a update_plot en intervalos regulares
animation = FuncAnimation(fig, update_plot, frames=range(len(x_values)), interval=200)

# Mostrar la animación
plt.show()
