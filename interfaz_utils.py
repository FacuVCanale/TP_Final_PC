
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from communication.client.client import MountainClient
import matplotlib.pyplot as plt
import customtkinter
from matplotlib.animation import FuncAnimation
import matplotlib

matplotlib.use('TkAgg')

class SecondFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.container_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container_frame.grid(row=0, column=0, sticky="nsew")
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)

        self.show_graf3D()

    
    def show_graf3D(self):
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_xlim3d(0, 20000)
        self.ax.set_ylim3d(0, 20000)
        self.ax.set_zlim3d(0, 5000)

        self.cliente = MountainClient("localhost", 8080)

        self.points = self.ax.scatter([], [], [], c='b', marker='o')

        self.ani = FuncAnimation(fig, self.update_graph, frames=10, interval=1000, blit=False, repeat=False)

        canvas = FigureCanvasTkAgg(fig, master=self.container_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.ani._start()

    def update_graph(self, frame):
        
        info = self.cliente.get_data()

        points = []
        for team, climbers in info.items():
            for climber, data in climbers.items():
                x = data['x']
                y = data['y']
                z = data['z']
                points.append((x, y, z))

        x, y, z = zip(*points)
        self.points.set_3d_properties(z, zdir='z') 
        self.points.set_offsets(np.column_stack((x, y)))
        
        return self.points,

