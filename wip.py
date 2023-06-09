import math
import random
import matplotlib.pyplot as plt
import numpy as np

radius = 23000
num_points = 100
points = []

for _ in range(num_points):
    difx = random.uniform(-1, 1)
    dify = random.uniform(-1, 1)
    x = radius * difx
    y = radius * dify
    
    # Generar valores de z utilizando diferentes funciones y escalares aleatorios
    z = 0
    num_functions = random.randint(3, 7)  # Cantidad aleatoria de funciones
    
    for _ in range(num_functions):
        function_type = random.randint(1, 3)  # Seleccionar aleatoriamente el tipo de función
        
        if function_type == 1:
            scalar = random.uniform(0.5, 2.0)  # Escalar aleatorio
            z += scalar * math.sin(x / radius * random.uniform(1.0, 3.0) * math.pi)  # Función seno
            
        elif function_type == 2:
            scalar = random.uniform(10, 50)  # Escalar aleatorio
            z += scalar * math.cos(y / radius * random.uniform(1.0, 3.0) * math.pi)  # Función coseno
            
        else:
            scalar = random.uniform(1, 5)  # Escalar aleatorio
            z += scalar * math.sin(x / radius * random.uniform(1.0, 3.0) * math.pi) * math.cos(y / radius * random.uniform(1.0, 3.0) * math.pi)  # Producto de funciones
            
    z += random.randint(20, 250)  # Valor constante añadido
    
    point = [x, y, z]
    points.append(point)

# Extraer las coordenadas x, y, y los valores z
x_coords = [point[0] for point in points]
y_coords = [point[1] for point in points]
z_values = [point[2] for point in points]

plt.scatter(x_coords, y_coords, c=z_values, cmap="BrBG_r")
plt.colorbar()
plt.title("Scatter Plot of (x, y) Coordinates")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
