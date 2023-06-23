import threading  
from tkinter import *  
import matplotlib  
matplotlib.use("TkAgg")  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
import matplotlib.pyplot as plt    
import numpy as np  
import time
from communication.client.client import MountainClient  

class Dashboard:
    def __init__(self, client: MountainClient):
        self.root = Tk()  # Crea una instancia de la clase Tk para crear la ventana principal
        self.root.title("Dashboard")  
        self.client = client  
        self.data = client.get_data()  
        self.time_step = 500  # ms 
        self.animations = []  # for animations to stay alive in memory - Lista para almacenar las animaciones y evitar que sean eliminadas por el recolector de basura
        self.figsize = (3, 3)  # Tamaño de la figura del gráfico

        # Crear la cuadrícula 4x4 para los elementos de la interfaz
        self.grid_frame = [[None] * 4 for _ in range(4)]  # Crea una lista 2D para almacenar los marcos de la cuadrícula

        # Configurar el gráfico
        self.fig = plt.figure(figsize=self.figsize)  # Crea una figura de matplotlib con el tamaño especificado
        self.ax = self.fig.add_subplot(111, projection='3d')  # Añade un subplot 3D a la figura
        self.scatter = None  # Variable para almacenar el objeto scatter (dispersión) del gráfico

    def visualization_example(self, frame, fig):
        # Mostrar el gráfico en la cuadrícula
        canvas = FigureCanvasTkAgg(fig, master=frame)  # Crea un lienzo de TkAgg para el gráfico de matplotlib
        canvas.draw()  # Dibuja el gráfico en el lienzo
        canvas.get_tk_widget().pack()  # Empaqueta el lienzo en el marco de la cuadrícula

    def start(self):
        # No modificar
        t = threading.Thread(target=self.update_data)  
        t.start() 
        self.root.mainloop()  

    def update_data(self):
        # No modificar
        while not self.client.is_over():
            self.data = self.client.get_data()  # Actualiza los datos del cliente
            self.update_plot()  # Llama al método para actualizar el gráfico
            time.sleep(self.time_step / 1000)  # Espera el tiempo especificado antes de la próxima actualización

    def update_plot(self):
        x_values = []  # Lista para almacenar los valores de la coordenada x
        y_values = []  # Lista para almacenar los valores de la coordenada y
        z_values = []  # Lista para almacenar los valores de la coordenada z

        # Leer las coordenadas del archivo
        with open('coordenadas.tsv', 'r') as file:
            for line in file:
                parts = line.strip().split(':')  
                if len(parts) == 4:  
                    coordinates = parts[3].strip().split(',')  
                    if len(coordinates) == 3: 
                        x, y, z = map(float, coordinates) 
                        x_values.append(x)  
                        y_values.append(y) 
                        z_values.append(z) 

        # Actualizar el gráfico con los nuevos datos
        if self.scatter is None:
            self.scatter = self.ax.scatter(x_values, y_values, z_values)  # Crea un nuevo objeto scatter si no existe uno
        else:
            self.scatter._offsets3d = (x_values, y_values, z_values)  # Actualiza las coordenadas del objeto scatter existente

        self.ax.set_xlim(min(x_values), max(x_values))  # Establece los límites del eje x del gráfico
        self.ax.set_ylim(min(y_values), max(y_values))  # Establece los límites del eje y del gráfico
        self.ax.set_zlim(min(z_values), max(z_values))  # Establece los límites del eje z del gráfico
        self.scatter.set_array(z_values)  # Establece los valores de color para el objeto scatter basado en z_values
        self.scatter.set_cmap('BrBG_r')  # Establece el mapa de colores para el objeto scatter

        self.fig.canvas.draw()  # Dibuja la figura del gráfico

    def stop(self):
        # No modificar
        self.root.quit()  # Cierra la ventana principal y finaliza la aplicación

# No modificar
if __name__ == "__main__":
    client = MountainClient('localhost', 8080) 
    d = Dashboard(client) 

    # Crear la cuadrícula 4x4 de marcos
    for i in range(4):
        for j in range(4):
            frame = Frame(d.root, borderwidth=2, relief="solid")  # Crea un nuevo marco con borde sólido
            frame.grid(row=i, column=j, padx=5, pady=5)  # Ubica el marco en la cuadrícula
            d.grid_frame[i][j] = frame  # Almacena el marco en la lista de la cuadrícula

    # Mostrar el gráfico en el primer casillero (fila 0, columna 0)
    d.visualization_example(d.grid_frame[0][0], d.fig)  # Llama al método para mostrar el gráfico en el marco especificado

    # Suponiendo
    escaladores = ["facu", "lucas", "juan"]
    for i, nombre in enumerate(escaladores):
        label = Label(d.grid_frame[1][0], text=nombre)  # Crea una etiqueta con el nombre del escalador
        label.pack()  # Empaqueta la etiqueta en el marco

    # Generar un gráfico aleatorio en el segundo casillero (fila 0, columna 1)
    fig_random = plt.figure(figsize=d.figsize)  # Crea una nueva figura para el gráfico aleatorio
    ax_random = fig_random.add_subplot(111)  # Añade un subplot a la figura
    random_values = np.random.randn(100)  # Genera valores aleatorios
    ax_random.plot(random_values)  # Crea el gráfico con los valores aleatorios
    d.visualization_example(d.grid_frame[0][1], fig_random)  # Llama al método para mostrar el gráfico en el marco especificado

    # Generar un gráfico de una función lineal en el tercer casillero (fila 0, columna 2)
    fig_lineal = plt.figure(figsize=d.figsize)  # Crea una nueva figura para el gráfico de función lineal
    ax_lineal = fig_lineal.add_subplot(111)  # Añade un subplot a la figura
    x_values = np.linspace(0, 10, 100)  # Genera valores de x
    y_values = 2 * x_values + 1  # Calcula los valores de y
    ax_lineal.plot(x_values, y_values)  # Crea el gráfico de la función lineal
    d.visualization_example(d.grid_frame[0][2], fig_lineal)  # Llama al método para mostrar el gráfico en el marco especificado

    d.start()  # Inicia la aplicación
