import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def mountain_function(x, y):
    # Componentes sinusoidales con diferentes frecuencias y amplitudes
    component1 = np.sin(0.5 * x + 0.5 * y) * 2
    component2 = np.sin(2 * x - y) * 1.5
    component3 = np.sin(3 * x + 0.5 * y) * 3

    return component1 + component2 + component3

# Crear una cuadrícula de puntos en el rango deseado
x_range = np.linspace(-5, 5, 100)
y_range = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x_range, y_range)

# Calcular los valores de z para cada punto en la cuadrícula
Z = mountain_function(X, Y)

# Crear una figura en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Graficar la montaña en 3D
ax.plot_surface(X, Y, Z, cmap='terrain')

# Personalizar los ejes y el aspecto visual
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Altura')
ax.set_title('Representación 3D de una montaña con picos diferentes')

# Mostrar la figura
plt.show()
