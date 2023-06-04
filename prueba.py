import math
import matplotlib.pyplot as plt
from communication.server.mountain.mishra_mountain import MishraBirdMountain


mont = MishraBirdMountain(0,10)

def plot_mountain(mon):
    x = []
    y = []
    z = []

    for i in range(-mon.base_radius, mon.base_radius + 1):
        for j in range(-mon.base_radius, mon.base_radius + 1):
            x.append(i)
            y.append(j)
            z.append(mon.get_height(i, j))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(x, y, z)
    plt.show()



plot_mountain(mont)