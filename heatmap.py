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
        self.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.container_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container_frame.grid(row=0, column=0, sticky="nsew")
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)
        self.client = MountainClient("localhost", 8080)
        self.info = self.client.get_data()
        self.show_heatmap()

    def update_heatmap(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        x_values = []
        y_values = []
        z_values = []
        
        for team, climbers in self.info.items():
            for climber, data in climbers.items():
                x_values.append(data['x'])
                y_values.append(data['y'])
                z_values.append(data['z'])
        
        data = {'x': x_values, 'y': y_values, 'z': z_values}
        df = pd.DataFrame(data)
        df_pivot = df.pivot('y', 'x', 'z')
        
        sns.heatmap(df_pivot, ax=ax, cmap='hot', cbar=True)
    
    def show_heatmap(self):
        self.update_heatmap()
        plt.show()
