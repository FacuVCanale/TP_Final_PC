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
import customtkinter
import os
from PIL import Image
from matplotlib.backend_bases import widgets
import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.animation import FuncAnimation
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from communication.client.client import MountainClient
import itertools
from ascii import ascii
import sys
from leaderboard import mandar_data
from customtkinter import CTkFrame, CTkLabel


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
        self.selected_team = 'Everyone'
        self.client = MountainClient("localhost", 8080)

        self.show_graf3D()
        self.create_scrollable_frame()

    def show_graf3D(self):
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_xlim3d(-23000, 20000)
        self.ax.set_ylim3d(-23000, 20000)
        
        self.points = self.ax.scatter([], [], [], c='green', marker='o')

        self.ani = FuncAnimation(fig, self.update_graph, interval=1000, blit=False, repeat=False)

        canvas = FigureCanvasTkAgg(fig, master=self.container_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.ani._start()

    def update_graph(self, frame):
        """
        Update the graph based on the data received from the server.

        Args:
            frame: The frame to update the graph on.

        Returns:
            The updated points object.

        """
        self.info = self.client.get_data()  # Update server data

        points = []
        for team, climbers in self.info.items():
            if self.selected_team == 'Everyone': #To show all the points (players) on the map
                for climber, data in climbers.items():
                    x = data['x']
                    y = data['y']
                    z = data['z']
                    points.append((x, y, z))
            elif team == self.selected_team:
                for climber, data in climbers.items():
                    x = data['x']
                    y = data['y']
                    z = data['z']
                    points.append((x, y, z))

        x, y, z = zip(*points) if points else ([], [], [])
        self.points.set_3d_properties(z, zdir='z')
        self.points.set_offsets(np.column_stack((x, y)))

        if points: 

            min_z, max_z = min(z), max(z)

            
            self.ax.set_zlim3d(0, max_z)

        return self.points,


    def get_team_list_from_server(self):
        """
        Retrieve the list of teams from the server data.

        Returns:
            A list of teams.

        """
        teams = []
        for team, climbers in self.info.items():
            teams.append(team)
        return teams


    def create_scrollable_frame(self):
        """
        Create and configure a scrollable frame to display the team list.

        """
        scrollable_frame = ScrollableLabelButtonFrame(self.container_frame)
        scrollable_frame.grid(row=0, column=1, sticky="nsew", padx=3, pady=3)

        teams = self.get_team_list_from_server()
        scrollable_frame.add_item("Everyone", command=self.select_team)

        for team in teams:
            scrollable_frame.add_item(team, command=self.select_team)

        scrollable_frame.configure(width=150, height=100)


    def select_team(self, team):
        """
        Update the selected team and update the graph accordingly.

        Args:
            team: The selected team.

        """
        self.selected_team = team
        self.update_graph(None)



class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        """
        Initialize the ScrollableLabelButtonFrame.

        Args:
            master: The master widget.
            command: Optional command function to be executed by the buttons.
            **kwargs: Additional keyword arguments to be passed to the parent class.

        """
        # Call the __init__ method of the parent class (customtkinter.CTkScrollableFrame)
        super().__init__(master, **kwargs)
        # Configure the first column of the grid to expand and fill any remaining space
        self.grid_columnconfigure(0, weight=1) #weight means the priority of the column if the space given has to be distributed among other columns.

        # Set the 'command' attribute of the instance to the provided 'command' argument
        self.command = command
        
        # Create an empty list to store label instances
        self.label_list = []
        # Create an empty list to store button instances
        self.button_list = []

    def add_item(self, item, image=None, command=None):
        """
        Add a label and button to the frame.

        Args:
            item: The text to display in the label.
            image: Optional image to display alongside the text.
            command: Optional command function to be executed by the button.

        """
        # Create a label instance with the provided 'item' as the text and optional 'image'
        label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        # Create a button instance with the text "Ver" and specified width and height
        button = customtkinter.CTkButton(self, text="Ver", width=30, height=24)
        # If a 'command' argument is provided, configure the button's command to execute it with 'item' as an argument
        if command is not None:
            button.configure(command=lambda: command(item))
        # Add the label to the grid at a new row based on the current length of 'label_list' and in the first column
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        # Add the button to the grid at a new row based on the current length of 'button_list' and in the second column
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        # Append the label to the 'label_list'
        self.label_list.append(label)
        # Append the button to the 'button_list'
        self.button_list.append(button)

    
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
        self.Z = np.zeros((100,100)) +1500

    """ RADIUS = 1.0  # Control this value.
ax1.set_xlim3d(-RADIUS / 2, RADIUS / 2)
ax1.set_zlim3d(-RADIUS / 2, RADIUS / 2)
ax1.set_ylim3d(-RADIUS / 2, RADIUS / 2) """

    def show_animation(self):
        res = 100

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
        #Z = np.zeros_like(X)

        

        # Funcion de inicializacion
        def init():
            return ax,

        # Funcion de actualizacion 
        def update(frame):
            nonlocal X, Y

            # Obtener los datos actualizados del cliente
            info = cliente.get_data()

            # Actualizar los valores de Z en la superficie
            for team, climbers in info.items():
                for climber, data in climbers.items():
                    x2 = data['x']
                    y2 = data['y']
                    z2 = data['z']

                    # Verificar si el punto ya existe en la lista de picos
                    
                    # Calcular las distancias entre los puntos (x, y) y (x2, y2) -> EUCLIDEAN
                    # Encontrar la posición del punto más cercano
                    idx_x = np.argmin(abs(x - x2))
                    idx_y = np.argmin(abs(y - y2))

                    # Asignar el valor de altura al punto correspondiente en Z
                    self.Z[idx_x, idx_y] = z2


            
            ax.set_xlabel("Eje X")
            ax.set_ylabel("Eje Y")
            ax.set_zlabel("Altura")
            ax.clear()  # Limpiar el eje antes de agregar la nueva superficie
            ax.plot_surface(X, Y, self.Z, cmap='coolwarm', linewidth=0)

            return ax,

        # Animacion
        animation = FuncAnimation(fig, update, frames=None, init_func=init, blit=False)

        # Create a Matplotlib canvas and display it in the container frame
        canvas = FigureCanvasTkAgg(fig, master=self.container_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)

class FourthFrame(customtkinter.CTkFrame):
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

        self.fig, self.ax = plt.subplots()
        self.heatmap = None  # Initialize the heatmap attribute
        self.canvas = None

    def update_heatmap(self, frame):
        self.ax.clear()
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

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Player Heatmap')

        if self.heatmap is None:
            self.heatmap = sns.heatmap(heatmap, cmap='viridis', xticklabels=False, yticklabels=False, ax=self.ax)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.container_frame)
            self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        else:
            self.heatmap.set_data(heatmap)
            self.heatmap.autoscale()

        self.canvas.draw()


    def show_animation(self):
        self.animation = FuncAnimation(self.fig, self.update_heatmap, interval=1000)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.container_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

class ThirdFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=1, sticky="nsew")
        self.state = False

        cliente = MountainClient("localhost",8080)
        info = cliente.get_data()
        num_jugador = 65
        self.letter_asig = {}
        counter = 0
        while cliente.is_registering_teams() or (counter == 0):
            for equipo, escaladores in info.items():
                self.letter_asig[equipo] = num_jugador
                num_jugador += 1
            counter += 1
        label_resultado = customtkinter.CTkLabel(self, text=ascii(self.letter_asig), font=('Helvetica', 10))
        label_resultado.pack()
        self.call_function()
        
    def change(self):
        self.state = True
        self.call_function()

    def call_function(self):
        for widgets in self.winfo_children():
            widgets.destroy()
        label_resultado = customtkinter.CTkLabel(self, text=ascii(self.letter_asig), font=('Helvetica', 10))
        label_resultado.pack()
        self.after(500,self.call_function)


class FifthFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=3, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)

        self.selected_team = 'Everyone'

        # create container frame with grid layout
        self.container_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container_frame.grid(row=0, column=0, sticky="nsew")
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)
        self.client = MountainClient("localhost", 8080)
        self.info = self.client.get_data()

        self.show_scatter()

        

    def show_scatter(self):
        fig, ax = plt.subplots()

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_xlim(-23000, 20000)
        ax.set_ylim(-23000, 20000)

        self.points = ax.scatter([], [], c='green', marker='o')

        self.animation = FuncAnimation(fig, self.update_scatter, interval=1000, blit=False, repeat=False)

        canvas = FigureCanvasTkAgg(fig, master=self.container_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.animation._start()

    def update_scatter(self, frame):
        """
        Update the scatter plot based on the data received from the server.

        Args:
            frame: The frame to update the scatter plot on.

        Returns:
            The updated points object.

        """
        self.info = self.client.get_data()  # Update server data

        points = []
        for team, climbers in self.info.items():
            if self.selected_team == 'Everyone':
                for climber, data in climbers.items():
                    x = data['x']
                    y = data['y']
                    points.append((x, y))
            elif team == self.selected_team:
                for climber, data in climbers.items():
                    x = data['x']
                    y = data['y']
                    points.append((x, y))

        x, y = zip(*points) if points else ([], [])
        self.points.set_offsets(np.column_stack((x, y)))

        return self.points,


    def show_animation(self):
        self.animation = FuncAnimation(self.fig, self.update_scatter, interval=1000)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.container_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")


        
        
        




