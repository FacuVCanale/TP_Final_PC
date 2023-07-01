import customtkinter
import os
from PIL import Image
from tpf_CLIFF_interface_utils import HikersPositionFrame,MountainGraphFrame,HeatmapFrame, ASCIIFrame, ScatterFrame,Leaderboard
from communication.client.client import MountainClient
import random
from typing import Dict
import argparse


# Initialize the Client
class App(customtkinter.CTk):
    def __init__(self, client: MountainClient) -> None:
        super().__init__()
        
        self.title("Server Dashboard")
        #self.resizable(False, False)

        width: int = self.winfo_screenwidth()
        height: int = self.winfo_screenheight()
        # setting tkinter window size
        self.geometry(f"{int(width)}x{int(height)}")
        #self.resizable(False, False)
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.team_colors: dict = {'Everyone': 'white'} # Meaningless
        self.client = client
        self.generate_color_for_each_team()


        # Load images with light and dark mode image
        image_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image: customtkinter.CTkImage = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(200, 70))

        self.mountain_image: customtkinter.CTkImage = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "mountain_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "mountain_light.png")), size=(80, 80))
        
        self.hikers_image: customtkinter.CTkImage = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "hikers_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "hikers_light.png")), size=(80, 80))
        
        self.ascii_image: customtkinter.CTkImage = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "ascii_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "ascii_light.png")), size=(80, 80))
        
        self.heatmap_image: customtkinter.CTkImage = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "heatmap_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "heatmap_light.png")), size=(80, 80))
        
        self.scatter_image: customtkinter.CTkImage = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "scatter_dark.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "scatter_light.png")), size=(80, 80))
        self.navigation_frame: customtkinter.CTkFrame = customtkinter.CTkFrame(self, corner_radius=0)

        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        # FRAME DE NAVEGACION
        self.navigation_frame_label: customtkinter.CTkLabel = customtkinter.CTkLabel(self.navigation_frame,
                                                                                     image=self.logo_image,
                                                                                     compound="left",
                                                                                     font=customtkinter.CTkFont(size=15, weight="bold"), text="")
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Leaderboard
        self.navigation_frame2: Leaderboard = Leaderboard(self.client)
        self.navigation_frame2.grid(row=0, column=2, sticky="nsew")
        self.navigation_frame2.grid_rowconfigure(1, weight=1)

        # FRAME MOUNTAIN
        self.home_button: customtkinter.CTkButton = customtkinter.CTkButton(self.navigation_frame,
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

        # HIKERS FRAME
        self.frame_2_button: customtkinter.CTkButton = customtkinter.CTkButton(self.navigation_frame,
                                                                               corner_radius=0,
                                                                               height=40,
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
        w: int = 1200
        h: int = 780

        # Change appearance of the GUI
        self.appearance_mode_menu: customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                    command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=40, sticky="s")

        # Create the 3D Frame
        self.home_frame: MountainGraphFrame = MountainGraphFrame(self, self.client, w, h)

        # Create Hikers Frame
        self.second_frame: HikersPositionFrame = HikersPositionFrame(self, self.client, self.team_colors, w, h)

        # create ASCII Frame
        self.third_frame: ASCIIFrame = ASCIIFrame(self, self.client, w, h)

        # Create Heatmap Frame
        self.fourth_frame: HeatmapFrame = HeatmapFrame(self, self.client, w, h)

        # Create Scatter Frame
        self.fifth_frame: ScatterFrame = ScatterFrame(self, self.client, self.team_colors, w, h)

        self.select_frame_by_name("home")

    def generate_color_for_each_team(self) -> None:
        """
        Generate a random color for each team in the data and store it in the `team_colors` dictionary.
        """
        self.info: Dict[str, list] = self.client.get_data() # type hint for self.info
        for team, climbers in self.info.items():
            color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
            self.team_colors[team] = color

    def select_frame_by_name(self, name: str) -> None:
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
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
            self.home_frame.show_graph()
        else:
            self.home_frame.grid_forget()

        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
            self.second_frame.show_graf3D()
        else:
            self.second_frame.grid_forget()

        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1,sticky="nsew")
            self.fourth_frame.show_animation()
        else:
            self.fourth_frame.grid_forget()

        if name == "frame_5":
            self.fifth_frame.grid(row=0, column=1, sticky="nsew")
            self.fifth_frame.show_scatter()
        else:
            self.fifth_frame.grid_forget()
            
    def home_button_event(self) -> None:
        """
        Event handler for the home button. Selects the home frame.
        """
        self.select_frame_by_name("home")

    def frame_2_button_event(self) -> None:
        """
        Event handler for the frame 2 button. Selects the frame 2.
        """
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self) -> None:
        """
        Event handler for the frame 3 button. Selects the frame 3.
        """
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self) -> None:
        """
        Event handler for the frame 4 button. Selects the frame 4 and shows its animation.
        """
        self.select_frame_by_name("frame_4")
        self.fourth_frame.show_animation()

    def frame_5_button_event(self) -> None:
        """
        Event handler for the frame 5 button. Selects the frame 5 and shows its animation.
        """
        self.select_frame_by_name("frame_5")
        self.fifth_frame.show_animation()

    def change_appearance_mode_event(self, new_appearance_mode: str) -> str:
        """
        Event handler for changing the appearance mode.

        Args:
            new_appearance_mode: The new appearance mode.

        Returns:
            The new appearance mode.
        """
        mode = customtkinter.set_appearance_mode(new_appearance_mode)
        return mode
    
def main():
    parser = argparse.ArgumentParser(description='Command line args')
    parser.add_argument('--ip', type=str, help='IP and port', default="localhost:8080")
    args = parser.parse_args()
    ip, port = args.ip.split(':')

    try:
        port = int(port)
    except:
        print("No ha ingresado un puerto válido")
        return None

    client = MountainClient(ip, port)
    app = App(client)
    app.mainloop()


if __name__ == "__main__":
    main()

