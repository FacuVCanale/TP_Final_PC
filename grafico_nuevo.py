import tkinter as tk
import pygame

def play_music():
    pygame.mixer.music.load("ruta_del_archivo_de_audio.mp3")
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

# Inicializar Pygame y el mezclador de música
pygame.mixer.init()

# Crear la ventana de Tkinter
window = tk.Tk()

# Botón para reproducir música
play_button = tk.Button(window, text="Play", command=play_music)
play_button.pack()

# Botón para detener la música
stop_button = tk.Button(window, text="Stop", command=stop_music)
stop_button.pack()

# Ejecutar el bucle principal de Tkinter
window.mainloop()
a
