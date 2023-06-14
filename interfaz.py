import time
import threading
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np

from communication.client.client import MountainClient

class Dashboard:
    def __init__(self, client: MountainClient):
        self.root = Tk()
        self.root.title("Dashboard")
        self.client = client
        self.data = client.get_data()
        self.time_step = 500  # ms
        self.animations = []  # for animations to stay alive in memory
        self.figsize = (4.5, 3)
        self.highest_climber_label = Label(self.root, text="")
        self.highest_climber_label.pack()

        # Crear un marco para mostrar el gráfico
        self.plot_frame = Frame(self.root)
        self.plot_frame.pack()

        # Configurar el gráfico
        self.fig = plt.figure(figsize=self.figsize)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.scatter = None

    def visualization_example(self, frame):
        # Mostrar el gráfico en el marco
        canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def start(self):
        # No modificar
        t = threading.Thread(target=self.update_data)
        t.start()
        self.root.mainloop()

    def update_data(self):
        # No modificar
        while not self.client.is_over():
            self.data = self.client.get_data()
            self.update_plot()
            self.update_highest_climber()  # Actualizar el escalador más alto
            time.sleep(self.time_step / 1000)

    def update_plot(self):
        x_values = []
        y_values = []
        z_values = []

        # Leer las coordenadas del archivo
        with open('coordenadas.txt', 'r') as file:
            for line in file:
                x, y, z = map(float, line.strip().split())
                x_values.append(x)
                y_values.append(y)
                z_values.append(z)

        # Actualizar el gráfico con los nuevos datos
        if self.scatter is None:
            self.scatter = self.ax.scatter(x_values, y_values, z_values)
        else:
            self.scatter._offsets3d = (x_values, y_values, z_values)

        self.ax.set_xlim(min(x_values), max(x_values))
        self.ax.set_ylim(min(y_values), max(y_values))
        self.ax.set_zlim(min(z_values), max(z_values))
        self.scatter.set_array(z_values)
        self.scatter.set_cmap('BrBG_r')

        self.fig.canvas.draw()

    def update_highest_climber(self):
        highest_climber = None
        highest_altitude = float('-inf')

        for team in self.data.values():
            for climber_name, climber in team.items():
                altitude = climber['z']
                if altitude > highest_altitude:
                    highest_climber = climber
                    highest_altitude = altitude

        if highest_climber is not None:
            name = highest_climber.get('name', 'Unknown')
            altitude = highest_climber['z']
            self.highest_climber_label.config(text=f"Highest climber: {name} ({altitude})")

    def stop(self):
        # No modificar
        self.root.quit()


if __name__ == "__main__":
    # No modificar
    client = MountainClient('localhost', 8080)
    d = Dashboard(client)
    d.visualization_example(plt.gca())
    d.start()


#10.42.0.1 8888 LINAR

#"34.16.147.147",8080 sv