import time
import threading
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from communication.client.client import MountainClient

class Dashboard:
    def __init__(self, client: MountainClient):
        self.root = Tk()  # Se crea la ventana principal de la interfaz gráfica
        self.root.title("Dashboard")  # Se establece el título de la ventana
        self.client = client
        self.time_step = 500  # ms
        self.figsize = (6, 3)

        # Crear un marco para mostrar el gráfico
        self.plot_frame = Frame(self.root)  # Se crea un marco en la ventana principal

        
        self.plot_frame.pack()  # Se empaqueta el marco para mostrarlo en la ventana

        # Configurar el gráfico
        self.fig = plt.figure(figsize=self.figsize)  # Se crea una figura de Matplotlib con un tamaño específico
        self.ax = self.fig.add_subplot(111, projection='3d')  # Se agrega un subgráfico 3D a la figura
        self.scatter = None  # Inicialmente no hay un gráfico de dispersión

    def visualization_example(self, frame):
        # Mostrar el gráfico en el marco
        canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)  # Se crea un objeto FigureCanvasTkAgg para dibujar la figura en el marco
        canvas.draw()  # Se dibuja la figura en el lienzo
        canvas.get_tk_widget().pack()  # Se empaqueta el widget del lienzo en el marco para mostrarlo en la ventana

    def start(self):
        # No modificar
        t = threading.Thread(target=self.update_data)  # Se crea un hilo para actualizar los datos
        t.start()  # Se inicia el hilo
        self.root.mainloop()  # Se inicia el bucle principal de la interfaz gráfica

    def update_data(self):
        # No modificar
        while not self.client.is_over():
            self.update_plot()  # Se actualiza el gráfico
            time.sleep(self.time_step / 1000)  # Se pausa la ejecución por el tiempo especificado

    def update_plot(self):
        x_values = []
        y_values = []
        z_values = []

        # Leer las coordenadas del archivo
        with open('coordenadas.txt', 'r') as file:  
            for line in file:  
                x, y, z = map(float, line.strip().split())  # Se convierten los valores de la línea a floats
                x_values.append(x)  # Se agregan los valores a la lista de coordenadas x
                y_values.append(y)  # Se agregan los valores a la lista de coordenadas y
                z_values.append(z)  # Se agregan los valores a la lista de coordenadas z

        # Actualizar el gráfico con los nuevos datos
        if self.scatter is None:
            self.scatter = self.ax.scatter(x_values, y_values, z_values)  # Se crea un nuevo gráfico de dispersión si no existe uno previo
        else:
            self.scatter._offsets3d = (x_values, y_values, z_values)  # Se actualizan las coordenadas del gráfico de dispersión existente

        self.ax.set_xlim(min(x_values), max(x_values))  # Se establecen los límites en el eje x
        self.ax.set_ylim(min(y_values), max(y_values))  # Se establecen los límites en el eje y
        self.ax.set_zlim(min(z_values), max(z_values))  # Se establecen los límites en el eje z
        self.scatter.set_array(z_values)  # Se establecen los valores de datos z en el gráfico de dispersión
        self.scatter.set_cmap('BrBG_r')  # Se establece el mapa de colores para el gráfico de dispersión

        self.fig.canvas.draw()  # Se dibuja la figura actualizada en el lienzo

    def stop(self):
        # No modificar
        self.root.quit()  # Se cierra la ventana principal y se detiene la ejecución

if __name__ == "__main__":
    # No modificar
    client = MountainClient('localhost', 8080)
    d = Dashboard(client)
    d.visualization_example(plt.gca())  # Se muestra un ejemplo de visualización
    d.start()  # Se inicia la aplicación
