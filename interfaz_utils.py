
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
        self.selected_team = None
        self.cliente = MountainClient("localhost", 8080)

        self.show_graf3D()
        self.create_scrollable_frame()

    def show_graf3D(self):
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_xlim3d(0, 20000)
        self.ax.set_ylim3d(0, 20000)
        self.ax.set_zlim3d(0, 20000)

        self.points = self.ax.scatter([], [], [], c='b', marker='o')

        self.ani = FuncAnimation(fig, self.update_graph, interval=1000, blit=False, repeat=False)

        canvas = FigureCanvasTkAgg(fig, master=self.container_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.ani._start()

    def update_graph(self, frame):
        self.info = self.cliente.get_data()  # Actualizar los datos del servidor

        points = []
        for team, climbers in self.info.items():
            if team == self.selected_team:
                for climber, data in climbers.items():
                    x = data['x']
                    y = data['y']
                    z = data['z']
                    points.append((x, y, z))

        x, y, z = zip(*points) if points else ([], [], [])
        self.points.set_3d_properties(z, zdir='z')
        self.points.set_offsets(np.column_stack((x, y)))

        return self.points,


    def get_team_list_from_server(self):
        teams = []
        for team, climbers in self.info.items():
                teams.append(team)
        return teams

    def create_scrollable_frame(self):
        scrollable_frame = ScrollableLabelButtonFrame(self.container_frame)
        scrollable_frame.grid(row=0, column=1, sticky="nsew", padx=3, pady=3)

        teams = self.get_team_list_from_server()

        for team in teams:
            scrollable_frame.add_item(team, command=self.select_team)

        scrollable_frame.configure(width=150, height=100)

    def select_team(self, team):
        self.selected_team = team
        self.update_graph(None)





class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None, command=None):  # Agregar argumento command
        label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        button = customtkinter.CTkButton(self, text="Ver", width=30, height=24)
        if command is not None:  # Utilizar el argumento command en lugar de self.command
            button.configure(command=lambda: command(item))  # Utilizar el argumento command en lugar de self.command
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return

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