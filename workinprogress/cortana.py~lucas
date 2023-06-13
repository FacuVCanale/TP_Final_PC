import tkinter as tk
import unicodedata

# Funciones definidas en el código


def función1():
    pass


def función2():
    pass


def función3():
    pass


def función4():
    pass


# Obtener una lista de las funciones definidas en el código
functions = [f for f in globals() if callable(globals()[f])]


def remove_accents(text):
    # Función para eliminar acentos de un texto
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')


def on_search(event=None):
    query = entry.get()
    # Buscar funciones que coincidan con la consulta del usuario sin tener en cuenta los acentos
    suggestions = [f for f in functions if remove_accents(
        query.lower()) in remove_accents(f.lower())]
    # Limpiar la lista de sugerencias
    listbox.delete(0, tk.END)
    # Agregar sugerencias a la lista
    for suggestion in suggestions:
        listbox.insert(tk.END, suggestion)


def on_select(event):
    # Obtener la función seleccionada por el usuario
    selection = event.widget.get(event.widget.curselection())
    # Aquí puedes agregar código para realizar alguna acción con la función seleccionada
    print(f"Función seleccionada: {selection}")


root = tk.Tk()
root.title("Interfaz de búsqueda")

frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor="n")

entry = tk.Entry(frame, font=("Courier", 18))
entry.place(relwidth=0.65, relheight=1)
entry.bind("<KeyRelease>", on_search)

button = tk.Button(frame, text="Buscar", font=(
    "Courier", 12), command=on_search)
button.place(relx=0.7, relwidth=0.3, relheight=1)

frame2 = tk.Frame(root)
frame2.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.6, anchor="n")

label = tk.Label(frame2, text="Sugerencias:", font=("Courier", 18))
label.pack()

listbox = tk.Listbox(frame2)
listbox.pack(fill=tk.BOTH, expand=True)
listbox.bind("<<ListboxSelect>>", on_select)

root.mainloop()
