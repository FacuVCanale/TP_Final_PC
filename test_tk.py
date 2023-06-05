import tkinter as tk
import datetime

class Dog:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def update_position(self, new_position):
        self.position = new_position

def log_timestamp_decorator(func):
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] - Function {func.__name__} was called.")
        return func(*args, **kwargs)
    return wrapper

@log_timestamp_decorator
def update_object_position(obj):
    new_position = entry_position.get() 
    with open('collect_data.txt', 'a') as f:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        s = f'[{timestamp}]:'
        f.write(s + new_position + '\n')

    obj.update_position(new_position)
    display_text.configure(state="normal")
    display_text.insert(tk.END, f"Nombre: {obj.name}\nPosición: {obj.position}\n\n")
    display_text.configure(state="disabled")

objects = [
    Dog("Firulais", "Jardín"),
    Dog("Max", "Patio"),
    Dog("Buddy", "Casa"),
]

window = tk.Tk()
window.title("Interfaz de la concha de tu madre")

# Estilos
bg_color = "#3b5998"  # Color de fondo
text_color = "#ffffff"  # Color de texto
font_style = "Helvetica"  # Estilo de fuente

window.configure(bg=bg_color)

# Crear contenedor principal
main_frame = tk.Frame(window, bg=bg_color)
main_frame.pack(padx=20, pady=20)

# Etiqueta de título
title_label = tk.Label(main_frame, text="Interfaz", font=(font_style, 16, "bold"), fg=text_color, bg=bg_color)
title_label.pack(pady=10)

# Contenedor para la información del objeto seleccionado
info_frame = tk.Frame(main_frame, bg=bg_color)
info_frame.pack()

label_name = tk.Label(info_frame, text="Nombre: ", font=(font_style, 12, "bold"), fg=text_color, bg=bg_color)
label_name.pack(side="top")

label_position = tk.Label(info_frame, text="Posición: ", font=(font_style, 12, "bold"), fg=text_color, bg=bg_color)
label_position.pack(side="left")

# Campo de entrada y botón de actualización
entry_position = tk.Entry(main_frame, font=(font_style, 12))
entry_position.pack(pady=10)

button_update = tk.Button(main_frame, text="Actualizar posición", font=(font_style, 12, "bold"), fg='red', bg="#1877f2", command=lambda: update_object_position(objects[0]))
button_update.pack()

# Área de texto
display_text = tk.Text(main_frame, font=(font_style, 12), width=40, height=10)
display_text.pack(pady=10)
display_text.configure(state="disabled")

@log_timestamp_decorator
def update_label_values(obj):
    label_name.configure(text="Nombre: " + obj.name)
    label_position.configure(text="Posición: " + obj.position)

@log_timestamp_decorator
def select_object(index):
    if index < len(objects):
        selected_object = objects[index]
        update_label_values(selected_object)
        button_update.configure(command=lambda: update_object_position(selected_object))

# Botones de selección de objeto
button_frame = tk.Frame(main_frame, bg=bg_color) # botones de selección de objeto
button_frame.pack(pady=10)

for i, obj in enumerate(objects):
    button_select = tk.Button(button_frame, text=obj.name, font=(font_style, 12), fg='red', bg="#4267B2", padx=10, pady=5, command=lambda index=i: select_object(index))
    button_select.pack(side="left", padx=5)

window.mainloop()
