import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

# Datos de ejemplo
x = np.random.rand(100)
y = np.random.rand(100)
z = np.sin(x * np.pi) * np.cos(y * np.pi)

# Definir una cuadrícula regular para la interpolación
res = 100
xi = np.linspace(min(x), max(x), res)
yi = np.linspace(min(y), max(y), res)
xi, yi = np.meshgrid(xi, yi)

# Interpolación de los datos
zi = griddata((x, y), z, (xi, yi), method='cubic')

# Crear la figura y el eje 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Graficar la superficie interpolada
ax.plot_surface(xi, yi, zi, cmap='coolwarm')

# Mostrar el gráfico
plt.show()
