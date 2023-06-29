import customtkinter
from customtkinter import CTkFrame
import os
from PIL import Image
from interfaz_utils import SecondFrame,HomeFrame,FourthFrame, ThirdFrame, FifthFrame
from leaderboard import show_leaderboard
from communication.client.client import MountainClient

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Dashboard")

        width= self.winfo_screenwidth()
        height= self.winfo_screenheight()
        #setting tkinter window size
        self.geometry("%dx%d" % (width, height))
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)


        self.client = MountainClient()

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(155, 64))

        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(80, 80))
        
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(80, 80))
        
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(80, 80))
        
        self.music_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "heatmap.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "heatmap.png")), size=(80, 80))
        
        self.music_image2 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "scatter.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "scatter.png")), size=(80, 80))
        
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)  # ELEGIR CUANTAS OPCIONES PONER EN EL LADO IZQUIERDO ES DECIR CUANTOS RECTANGULOS
          # ELEGIR CUANTAS OPCIONES PONER EN EL LADO IZQUIERDO ES DECIR CUANTOS RECTANGULOS
        self.navigation_frame2 = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame2.grid(row=0, column=2, sticky="nsew")
        self.navigation_frame2.grid_rowconfigure(1, weight=1)
        #FRAME DE NAVEGACION
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame,
                                                             image=self.logo_image,  # ELEGIR NOMBRE DE LA BARRA DE TAREAS
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"), text="")
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.navigation_frame_label2 = customtkinter.CTkLabel(self.navigation_frame2,
                                                              # ELEGIR NOMBRE DE LA BARRA DE TAREAS
                                                             compound="right",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"), text=show_leaderboard())
        self.navigation_frame_label2.grid(row=0, column=0, padx=20, pady=20)
        self.call_function()
        #FRAME 3D
        self.home_button = customtkinter.CTkButton(self.navigation_frame, 
                                                   corner_radius=0, 
                                                   height=40, 
                                                   border_spacing=10,
                                                   text="MOUNTAIN", 
                                                   fg_color="transparent", 
                                                   text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.chat_image, 
                                                   anchor="w", 
                                                   command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        #FRAME 2D
        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, 
                                                      text="HIKERS",
                                                      fg_color="transparent", 
                                                      text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.home_image, 
                                                      anchor="w", 
                                                      command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        #FRAME ASCII
        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, 
                                                      text="ASCII",
                                                      fg_color="transparent", 
                                                      text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, 
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
                                                      image=self.music_image, 
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
                                              image=self.music_image2, 
                                              anchor="w", 
                                              command=self.frame_5_button_event)
        self.frame_5_button.grid(row=5, column=0, sticky="ew")


    
        #CAMBIAR APARIENCIA
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=20, sticky="s")


        # create home frame
        self.home_frame = HomeFrame(self,self.client)
        

        # create second frame
        self.second_frame = SecondFrame(self,self.client)

        
        # create third frame
        self.third_frame = ThirdFrame(self,self.client)

        self.fourth_frame =FourthFrame(self,self.client)
                  


        


        self.fifth_frame = FifthFrame(self)
                  


        self.select_frame_by_name("home")

    def call_function(self):
        for widgets in self.navigation_frame2.winfo_children():
            widgets.destroy()
        self.navigation_frame_label2 = customtkinter.CTkLabel(self.navigation_frame2,
                                                              # ELEGIR NOMBRE DE LA BARRA DE TAREAS
                                                             compound="right",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"), text=show_leaderboard())
        self.navigation_frame_label2.grid(row=0, column=0, padx=20, pady=20)
        self.after(5000,self.call_function)
        return
    #CAMBIAR DE PESTAÑAS - MODIFICO LA VISUALIZACION DE CADA PESTAÑA
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        self.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")
        
        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")   
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1,sticky="nsew")
            self.fourth_frame.show_animation()  # Call the show_animation method
        else:
            self.fourth_frame.grid_forget()

        if name == "frame_5":
            self.fifth_frame.grid(row=0, column=1, sticky="nsew")
            self.fifth_frame.show_animation()
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
    app.mainloop()
