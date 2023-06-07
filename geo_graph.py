import matplotlib.pyplot as plt

# Configura el grafico 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


x_values = []
y_values = []
z_values = []

# Crear la gráfica de puntos en 3D
scatter = ax.scatter(x_values, y_values, z_values)

# Función para actualizar el gráfico
def update_plot():
    
    with open('coordenadas.txt', 'r') as file:

        # Vacio las listas de datos existentes para que no se me agreguen de vuelta los datos que ya tengo y solo se agreguen los nuevos :)
        x_values.clear()
        y_values.clear()
        z_values.clear()

        # Lee cada linea del archivo y agrega los valores a las listas correspondientes
        for line in file:
            x, y, z = map(float, line.strip().split())
            x_values.append(x)
            y_values.append(y)
            z_values.append(z)

    # Actualizar la grafica con los datos que va recibiendo del SERVER ANAShje
    scatter._offsets3d = (x_values, y_values, z_values)

    # Ajusta los límites de los ejes para que no queden afuera los nuevos puntitos :(
    ax.set_xlim(min(x_values), max(x_values))
    ax.set_ylim(min(y_values), max(y_values))
    ax.set_zlim(min(z_values), max(z_values))

    # Actualiza el color de los puntos en función de sus alturas
    scatter.set_array(z_values)
    scatter.set_cmap('BrBG_r')

    # Actualiza el gráfico
    fig.canvas.draw()

# Bucle para actualizar el graficoooooooooooooo 
while True:
    update_plot()
    plt.pause(1)  # Pausa de 1 segundo para permitir la actualización del gráfico
