import customtkinter
import os
from PIL import Image
import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.animation import FuncAnimation
import numpy as np
from customtkinter import CTkFrame
from mpl_toolkits.mplot3d import Axes3D
from communication.client.client import MountainClient
import itertools


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("image_example.py")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))

        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))

        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))

        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        
        self.music_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)  # ELEGIR CUANTAS OPCIONES PONER EN EL LADO IZQUIERDO ES DECIR CUANTOS RECTANGULOS


        #FRAME DE NAVEGACION
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, 
                                                             text="Lucas pete",
                                                             image=self.logo_image,  # ELEGIR NOMBRE DE LA BARRA DE TAREAS
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        #FRAME 3D
        self.home_button = customtkinter.CTkButton(self.navigation_frame, 
                                                   corner_radius=0, 
                                                   height=40, 
                                                   border_spacing=10,
                                                   text="3D", 
                                                   fg_color="transparent", 
                                                   text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, 
                                                   anchor="w", 
                                                   command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        #FRAME 2D
        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, 
                                                      text="Posicion Hikers",
                                                      fg_color="transparent", 
                                                      text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, 
                                                      anchor="w", 
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        #FRAME TROLL
        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, 
                                                      text="TROLL",
                                                      fg_color="transparent", 
                                                      text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, 
                                                      anchor="w", 
                                                      command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        #FRAME PONER MUSICA 
        self.music_playing = False
        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, 
                                                      text="Gráfico Estimado de la Montaña ",
                                                      fg_color="transparent", 
                                                      text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, 
                                                      anchor="w", 
                                                      command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")




        #CAMBIAR APARIENCIA
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        #create first frame



        # create second frame
        self.second_frame = SecondFrame(self)

        
        # create third frame
        self.third_frame = ThirdFrame(self)
        
        #create fourth frame
        self.fourth_frame = FourthFrame(self)
        
          


        self.select_frame_by_name("home")
    
        

        pygame.mixer.init()

    #def music_button_event(self):
        

    #CAMBIAR DE PESTAÑAS - MODIFICO LA VISUALIZACION DE CADA PESTAÑA
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray20", "gray25") if name == "frame_4" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
            self.second_frame.ani._start()
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")
        self.fourth_frame.show_animation() 
        

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

class SecondFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)

        # Crear la figura y el gráfico 3D
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Configurar los límites del gráfico
        self.ax.set_xlim3d(0, 20000)
        self.ax.set_ylim3d(0, 20000)
        self.ax.set_zlim3d(0, 5000)

        # Crear la instancia del cliente
        self.cliente = MountainClient("localhost", 8080)

        # Crear la animación (dejar el resto del código intacto)
        self.ani = FuncAnimation(self.fig, self.update_graph, frames=itertools.count(), interval=1000)  # Intervalo en milisegundos

        # Crear el canvas y dibujar el gráfico inicial (dejar el resto del código intacto)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Iniciar la animación
        self.ani._start()

    def update_graph(self, frame):
        # Obtener los datos del cliente
        info = self.cliente.get_data()

        # Recorrer los datos y extraer las coordenadas
        points = []
        for team, climbers in info.items():
            for climber, data in climbers.items():
                x = data['x']
                y = data['y']
                z = data['z']

                # Agregar el punto a la lista
                points.append((x, y, z))

        # Limpiar el gráfico de dispersión
        self.ax.cla()

        # Actualizar el gráfico de dispersión con los nuevos puntos
        self.ax.scatter(*zip(*points))

        # Configurar los límites del gráfico
        self.ax.set_xlim3d(0, 20000)
        self.ax.set_ylim3d(0, 20000)
        self.ax.set_zlim3d(0, 5000)

        # Redibujar el gráfico en el canvas
        self.fig.canvas.draw()



class ThirdFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)

        # create container frame with grid layout
        self.container_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container_frame.grid(row=0, column=0, sticky="nsew")
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)

        self.button1 = customtkinter.CTkButton(self.container_frame, corner_radius=10, height=40, border_spacing=10,
                                              text="imagen", fg_color="transparent", text_color=("gray10", "gray90"),
                                              hover_color=("gray70", "gray30"), command=self.button1_event)
        self.button1.grid(row=0, column=0)

        self.music_playing = False  # Add the 'music_playing' attribute

    def button1_event(self):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        image = Image.open(os.path.join(image_path, "g.png"))
        if hasattr(self, "image_label"):
            self.image_label.grid_forget()  # Oculta la etiqueta de la imagen anterior
        self.image_label = customtkinter.CTkLabel(self.container_frame, image=customtkinter.CTkImage(image, size=(800, 600)))
        self.image_label.grid(row=0, column=0)
        if not self.music_playing:
            pygame.mixer.music.load("ctk/test_images/song.mp3")
            pygame.mixer.music.play(-1)  # Reproduce la música en bucle (-1 indica bucle infinito)
            self.music_playing = True
        else:
            pygame.mixer.music.stop()  # Detiene la reproducción de música
            self.music_playing = False


class FourthFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=2, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)

        # create container frame with grid layout
        self.container_frame = CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container_frame.grid(row=0, column=0, sticky="nsew")
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)

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
        Z = np.zeros_like(X)

        # Funcion de inicializacion
        def init():
            return ax,

        # Funcion de actualizacion 
        def update(frame):
            nonlocal X, Y, Z

            # Obtener los datos actualizados del cliente
            info = cliente.get_data()

            # Actualizar los valores de Z en la superficie
            for team, climbers in info.items():
                for climber, data in climbers.items():
                    x2 = data['x']
                    y2 = data['y']
                    z2 = data['z']

                    # Calcular las distancias entre los puntos (x, y) y (x2, y2) -> EUCLIDEAN
                    # Encontrar la posición del punto más cercano
                    idx_x = np.argmin(abs(x - x2))
                    idx_y = np.argmin(abs(y - y2))

                    # Asignar el valor de altura al punto correspondiente en Z
                    Z[idx_x, idx_y] = z2

            ax.clear()  # Limpiar el eje antes de agregar la nueva superficie
            ax.plot_surface(X, Y, Z, cmap='coolwarm', linewidth=0)

            return ax,

        # Animacion
        animation = FuncAnimation(fig, update, frames=None, init_func=init, blit=False)

        # Create a Matplotlib canvas and display it in the container frame
        canvas = FigureCanvasTkAgg(fig, master=self.container_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)

       
        

    

if __name__ == "__main__":
    app = App()
    app.mainloop()
