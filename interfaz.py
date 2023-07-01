import customtkinter
import os
from PIL import Image
from interfaz_utils import HikersPositionFrame,MountainGraphFrame,HeatmapFrame, ASCIIFrame, ScatterFrame,Leaderboard
from communication.client.client import MountainClient
import random

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Server Dashboard")
        self.resizable(False, False)

        width= self.winfo_screenwidth()
        height= self.winfo_screenheight()
        #setting tkinter window size
        self.geometry("%dx%d" % (width/1.4, height/1.4))
        self.resizable(False, False)
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.team_colors = {'Everyone': 'white'}
        self.client = MountainClient()
        self.generate_color_for_each_team()


        # Load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(200, 70))

        self.mountain_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "mountain_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "mountain_light.png")), size=(80, 80))
        
        self.hikers_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "hikers_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "hikers_light.png")), size=(80, 80))
        
        self.ascii_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "ascii_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "ascii_light.png")), size=(80, 80))
        
        self.heatmap_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "heatmap_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "heatmap_light.png")), size=(80, 80))
        
        self.scatter_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "scatter_dark.png")),dark_image=Image.open(os.path.join(image_path, "scatter_light.png")), size=(80, 80))



        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)

        
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)  # ELEGIR CUANTAS OPCIONES PONER EN EL LADO IZQUIERDO ES DECIR CUANTOS RECTANGULOS


        
       

        #FRAME DE NAVEGACION
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame,
                                                             image=self.logo_image,  # ELEGIR NOMBRE DE LA BARRA DE TAREAS
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"), text="")
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)


        #Leaderboard
        self.navigation_frame2 = Leaderboard(self.client)
        self.navigation_frame2.grid(row=0, column=2, sticky="nsew")
        self.navigation_frame2.grid_rowconfigure(1, weight=1)
        
        #FRAME 3D
        self.home_button = customtkinter.CTkButton(self.navigation_frame, 
                                                   corner_radius=0, 
                                                   height=40, 
                                                   border_spacing=10,
                                                   text="MOUNTAIN", 
                                                   fg_color="transparent", 
                                                   text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.mountain_image, 
                                                   anchor="w", 
                                                   command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        # 2D FRAME
        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, 
                                                      text="HIKERS",
                                                      fg_color="transparent", 
                                                      text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.hikers_image, 
                                                      anchor="w", 
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        # ASCII FRAME
        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, 
                                                      text="ASCII",
                                                      fg_color="transparent", 
                                                      text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.ascii_image, 
                                                      anchor="w", 
                                                      command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        #HEATMAP
        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, 
                                                      text="HEATMAP",
                                                      fg_color="transparent", 
                                                      text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.heatmap_image, 
                                                      anchor="w", 
                                                      command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        #SCATTER
        self.frame_5_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                              border_spacing=10, 
                                              text="SCATTER",
                                              fg_color="transparent", 
                                              text_color=("gray10", "gray90"),
                                              hover_color=("gray70", "gray30"),
                                              image=self.scatter_image, 
                                              anchor="w", 
                                              command=self.frame_5_button_event)
        self.frame_5_button.grid(row=5, column=0, sticky="ew")



        w = 1200
        h = 780

        #CAMBIAR APARIENCIA
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=40, sticky="s")


        # Create the 3D Frame
        self.home_frame = MountainGraphFrame(self,self.client,w,h)
        

        # Create Hikers Frame
        self.second_frame = HikersPositionFrame(self,self.client,self.team_colors,w,h)

        
        # create ASCII Frame
        self.third_frame = ASCIIFrame(self,self.client,w,h)

        # Create Heatmap Frame
        self.fourth_frame =HeatmapFrame(self,self.client,w,h)
        
        # Create Scatter Frame
        self.fifth_frame = ScatterFrame(self,self.client,self.team_colors,w,h)
                  


        self.select_frame_by_name("home")

     
 
    
    def generate_color_for_each_team(self):
        """
        Generate a random color for each team in the data and store it in the `team_colors` dictionary.
        """
        self.info = self.client.get_data()
        for team, climbers in self.info.items():            
            color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
            self.team_colors[team] = color

   
    #CAMBIAR DE PESTAÑAS - MODIFICO LA VISUALIZACION DE CADA PESTAÑA
    def select_frame_by_name(self, name):
        """
        Show the selected frame and change the appearance of the corresponding button.

        Args:
            name: The name of the frame to be selected.
        """

        # Change button color for the selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        self.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")
        
        # Show or hide selected frames based on the given name
        if name == "home": #3D
            self.home_frame.grid(row=0, column=1, sticky="nsew")
            self.home_frame.show_graph()
        else:
            self.home_frame.grid_forget()

        if name == "frame_2": #SCATTER
            self.second_frame.grid(row=0, column=1, sticky="nsew")
            self.second_frame.show_graf3D()   
        else:
            self.second_frame.grid_forget()

        if name == "frame_3": #ASCII
            self.third_frame.grid(row=0, column=1, sticky="nsew")
            
            
        else:
            self.third_frame.grid_forget()

        if name == "frame_4": #HEATMAP
            self.fourth_frame.grid(row=0, column=1,sticky="nsew")
            self.fourth_frame.show_animation()
        else:
            self.fourth_frame.grid_forget()

        if name == "frame_5": #2D
            self.fifth_frame.grid(row=0, column=1, sticky="nsew")
            self.fifth_frame.show_scatter()
        else:
            self.fifth_frame.grid_forget()
            
        

    def home_button_event(self):
        self.select_frame_by_name("home")
        

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")
        self.fourth_frame.show_animation()
    
    def frame_5_button_event(self):
        self.select_frame_by_name("frame_5")
        self.fifth_frame.show_animation()       
        

    def change_appearance_mode_event(self, new_appearance_mode):
        mode = customtkinter.set_appearance_mode(new_appearance_mode)
        return mode

if __name__ == "__main__":
    app = App()
    app.mainloop()#arreglar cuando cierra server
