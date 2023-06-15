import time
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = None

def update_plot(x_values, y_values, z_values):
    global scatter, ax

    # Actualizar el gráfico con los nuevos datos
    if scatter is None:
        scatter = ax.scatter(x_values, y_values, z_values)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
    else:
        scatter._offsets3d = (x_values, y_values, z_values)

    ax.set_xlim(min(x_values), max(x_values))
    ax.set_ylim(min(y_values), max(y_values))
    ax.set_zlim(min(z_values), max(z_values))
    scatter.set_array(z_values)
    scatter.set_cmap('BrBG_r')

    plt.draw()

def update_plot_continuously():
    global scatter, ax

    while True:
      
        x_values = [1.0, 2.0, 3.0]  # ejemplo
        y_values = [4.0, 5.0, 6.0]
        z_values = [7.0, 8.0, 9.0]

        update_plot(x_values, y_values, z_values)

        plt.pause(4)  


update_plot_continuously()
plt.show()
