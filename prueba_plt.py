import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

def generate_heatmap(data:dict):
    points = []

    for team, team_info in data.items():
        for hiker, hiker_info in team_info.items():
            point = (hiker_info["x"], hiker_info["y"])
            points.append(point)

    fig, ax = plt.subplots()

    # Crear círculo exterior de radio 23000
    outer_circle = plt.Circle((0, 0), radius=23000, color='purple')
    ax.add_artist(outer_circle)

    # Calcular la frecuencia de cada punto
    unique_points, counts = np.unique(points, axis=0, return_counts=True)

    # Crear cuadrados con colores según la cantidad de jugadores
    for point, count in zip(unique_points, counts):
        x = point[0]
        y = point[1]
        color = 'yellow' if count <= 2 else 'green' if count <= 5 else 'white'  # Cambia los colores según tus necesidades
        square = Rectangle((x - 500, y - 500), 1000, 1000, color=color)
        ax.add_artist(square)

    ax.set_aspect('equal', adjustable='box')
    plt.xlim(-25000, 25000)
    plt.ylim(-25000, 25000)
    plt.axis('off')
    plt.show()


data = {'CLIFF': 
            {'lucas': 
                {'x': 13096.168354203732, 
                 'y': 13572.11174816639, 
                 'z': 1730.7399040718012, 
                 'inclinacion_x': -94.47786207834619, 
                 'inclinacion_y': 26.005672776980468, 
                 'cima': False}, 
            'facu': 
                {'x': 13029.857499854661, 
                 'y': 14242.535625036326, 
                 'z': 1740.8850974550742, 
                 'inclinacion_x': -92.93106865087678, 
                 'inclinacion_y': 25.06745339748818, 
                 'cima': False}, 
            'fran': 
                {'x': 13572.11174816639, 
                 'y': 13096.168354203739, 
                 'z': 1705.2251654982615, 
                 'inclinacion_x': -98.7716711300381,
                 'inclinacion_y': 27.345122808129602, 
                 'cima': False}, 
            'ivan': 
            {'x': 14242.535625036326, 
             'y': 13029.857499854661, 
             'z': 1674.8863335572773, 
             'inclinacion_x': -103.87146277493585, 
             'inclinacion_y': 28.48029991065124, 
             'cima': False}}}

generate_heatmap(data)
