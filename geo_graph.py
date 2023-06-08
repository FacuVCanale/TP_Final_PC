import matplotlib.pyplot as plt

def mostrar_grafico():
    # Configura el gráfico 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_values = []
    y_values = []
    z_values = []

    # Crear la gráfica de puntos en 3D
    scatter = ax.scatter(x_values, y_values, z_values)

    # Función para actualizar el gráfico
    def update_plot():
        nonlocal x_values, y_values, z_values
        
        with open('coordenadas.txt', 'r') as file:
            # Vaciar las listas de datos existentes
            x_values.clear()
            y_values.clear()
            z_values.clear()

            # Leer cada línea del archivo y agregar los valores a las listas correspondientes
            for line in file:
                x, y, z = map(float, line.strip().split())
                x_values.append(x)
                y_values.append(y)
                z_values.append(z)

        # Actualizar la gráfica con los datos que se reciben del servidor
        scatter._offsets3d = (x_values, y_values, z_values)

        # Ajustar los límites de los ejes
        ax.set_xlim(min(x_values), max(x_values))
        ax.set_ylim(min(y_values), max(y_values))
        ax.set_zlim(min(z_values), max(z_values))

        # Actualizar el color de los puntos en función de sus alturas
        scatter.set_array(z_values)
        scatter.set_cmap('BrBG_r')

        # Actualizar el gráfico
        fig.canvas.draw()

    # Bucle para actualizar el gráfico
    while True:
        update_plot()
        plt.pause(1)  # Pausa de 1 segundo para permitir la actualización del gráfico
