import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def graficar_montana():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    montana = []
    min_z = float("inf")
    max_z = float("-inf")
    while True:
        entrada = input(
            "Ingresa los valores de x, y y z separados por comas o 'z' para salir: ")
        if entrada == "z":
            break
        x, y, z = map(int, entrada.split(","))
        montana.append((x, y, z))
        min_z = min(min_z, z)
        max_z = max(max_z, z)
    norm = plt.Normalize(min_z, max_z)
    for x, y, z in montana:
        color = cm.ScalarMappable(norm=norm, cmap="RdYlGn").to_rgba(z)
        ax.scatter(x, y, z, color=color)
    plt.show()


graficar_montana()
