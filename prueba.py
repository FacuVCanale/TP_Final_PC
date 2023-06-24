import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from communication.client.client import MountainClient
import customtkinter
import seaborn as sns

matplotlib.use('TkAgg')

class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=2, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)

        # create container frame with grid layout
        self.container_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container_frame.grid(row=0, column=0, sticky="nsew")
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)
        self.cliente = MountainClient("localhost", 8080)
        self.info = self.cliente.get_data()

    def show_animation(self):
        res = 100

        # Crear el rango de valores para los ejes x e y
        x = np.linspace(-23000, 23000, res)
        y = np.linspace(-23000, 23000, res)
        points = []
        for team, climbers in self.info.items():
            for climber, data in climbers.items():
                x2 = data['x']
                y2 = data['y']
                points.append((x2, y2))
        heatmap, _, _ = np.histogram2d(np.array(points)[:, 0], np.array(points)[:, 1], bins=(x, y))

        sns.heatmap(heatmap, cmap='viridis', xticklabels=False, yticklabels=False)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Player Heatmap')
        plt.show()
