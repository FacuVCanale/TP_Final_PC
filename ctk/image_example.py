import customtkinter
import os
from PIL import Image
import pygame

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.music_playing = False

    def play_music(self):
        if not self.music_playing:
            pygame.mixer.music.load("ctk/test_images/song.mp3")
            pygame.mixer.music.play(-1)  # Reproduce la música en bucle (-1 indica bucle infinito)
            self.music_playing = True
        else:
            pygame.mixer.music.stop()  # Detiene la reproducción de música
            self.music_playing = False

class ImageViewer:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.image_label = None

    def show_image(self):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        image = Image.open(os.path.join(image_path, "g.png"))
        if self.image_label is not None:
            self.image_label.grid_forget()  # Oculta la etiqueta de la imagen anterior
        self.image_label = customtkinter.CTkLabel(self.parent_frame, image=customtkinter.CTkImage(image, size=(800, 600)))
        self.image_label.grid(row=0, column=0)

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
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        # Music button
        self.music_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   image=self.music_image, text="Music",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   command=self.music_button_event)
        self.music_button.grid(row=6, column=0, sticky="ew")
        
        # create main content frame
        self.main_content_frame = customtkinter.CTkFrame(self, corner_radius=10, bg_color="gray90")
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")

        # create second frame in main content frame
        self.second_frame = customtkinter.CTkFrame(self.main_content_frame, corner_radius=10, bg_color="gray70")
        self.second_frame.grid(sticky="nsew")

        # create music player
        self.music_player = MusicPlayer()

        # create image viewer
        self.image_viewer = ImageViewer(self.second_frame)

        # create buttons
        self.button1 = customtkinter.CTkButton(self.second_frame, corner_radius=10, height=40, border_spacing=10,
                                               text="Show Image", fg_color="transparent", text_color=("gray10", "gray90"),
                                               hover_color=("gray70", "gray30"), command=self.button1_event)
        self.button1.grid(row=0, column=0)

        self.button2 = customtkinter.CTkButton(self.second_frame, corner_radius=10, height=40, border_spacing=10,
                                               text="Play Music", fg_color="transparent", text_color=("gray10", "gray90"),
                                               hover_color=("gray70", "gray30"), command=self.button2_event)
        self.button2.grid(row=1, column=0)

        self.button3 = customtkinter.CTkButton(self.second_frame, corner_radius=10, height=40, border_spacing=10,
                                               text="Stop Music", fg_color="transparent", text_color=("gray10", "gray90"),
                                               hover_color=("gray70", "gray30"), command=self.button3_event)
        self.button3.grid(row=2, column=0)

    def button1_event(self):
        self.image_viewer.show_image()

    def button2_event(self):
        self.music_player.play_music()

    def button3_event(self):
        self.music_player.play_music()

    def music_button_event(self):
        self.music_player.play_music()

if __name__ == "__main__":
    app = App()
    app.mainloop()
