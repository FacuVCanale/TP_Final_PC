import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt
import math

class Hiker:
    def __init__(self, name:str, pos:tuple, base_radius=23000, strat:str="default"):
        self.name = name
        self.pos = pos
        self.strat = strat
        self.points = []
        self.radius = base_radius

    def set_strat(self, strat):
        self.strat = strat
    
    def set_points(self, point):
        self.points.append(point)

    def start_strat(self):
        if self.strat == "default":
            self.alpha = 0.01 #learning rate
            self.beta = 0.5 #momentum
            self.momentum = [0,0]
        elif self.strat == "random":
            pass
        elif self.strat == "follow_points":
            pass
    
    def angle_from_xys(self, new_coords):
        delta_xy = (new_coords[0] - self.pos[0], new_coords[1] - self.pos[1])
        angle_rad = math.atan2(delta_xy[1], delta_xy[0])
        return angle_rad

    def move(self):
        if self.strat == "default":
            self.momentum[0] = self.beta * self.momentum[0] + self.pos[3]
            self.momentum[1] = self.beta * self.momentum[1] + self.pos[4]
            new_xy = (self.pos[0] - self.alpha * self.momentum[0], self.pos[1] - self.alpha * self.momentum[1])
            angle = self.angle_from_xys(new_xy)
            self.pos[0], self.pos[1] = self.pos[0] + self.radius * 50/23000 * math.cos(angle), self.pos[1] + self.radius * 50/23000 * math.sin(angle)
        elif self.strat == "follow_points":
            angle = self.angle_from_xys(self.points[0])
            self.pos[0], self.pos[1] = self.pos[0] + self.radius * 50/23000 * math.cos(angle), self.pos[1] + self.radius * 50/23000 * math.sin(angle)
            if self.pos[0] == self.points[0][0] and self.pos[1] == self.points[0][1]:
                self.points.pop(0)
            
    
    def __getitem__(self, index:int):
        return self.pos[index]
    
    def __setitem__(self, index:int, value:float):
        self.pos[index] = value
    
    def update_z_dx_dy(self, z, dx, dy):
        self.pos[2] = z
        self.pos[3] = dx
        self.pos[4] = dy

    
def mishra_bird_function_creator(base_radius):
    def mishra_bird_function(x: float, y: float) -> float:
        x = x / base_radius * 5
        y = y / base_radius * 5
        x = x - 5
        y = y - 5
        f = np.sin(y) * np.exp((1-np.cos(x))**2) + np.cos(x) * np.exp((1-np.sin(y))**2) + (x-y)**2 - 100
        return -f
    return mishra_bird_function

def mishra_bird_gradient_function_creator(base_radius):
    def mishra_bird_function_gradient(x: float, y: float) -> Tuple[float, float]:
        x = x / base_radius * 5
        y = y / base_radius * 5
        x = x - 5
        y = y - 5
        dfdx = 2*(x-y) + np.sin(y) * np.exp((1-np.cos(x))**2) * 2 * (1-np.cos(x)) * np.sin(x) - np.sin(x) * np.exp((1-np.sin(y))**2)
        dfdy = 2*(y-x) - np.cos(x) * np.exp((1-np.sin(y))**2) * 2 * (1-np.sin(y)) * np.cos(y) + np.cos(y) * np.exp((1-np.cos(x))**2)
        return -dfdx, -dfdy   # GRADIENT VECTOR
    return mishra_bird_function_gradient

radius = 115

function = mishra_bird_function_creator(radius)
dxdy = mishra_bird_gradient_function_creator(radius)

current_pos = [70, 70, -function(70,70), -dxdy(70,70)[0], -dxdy(70,70)[1]]
momentum_x = 0 
momentum_y = 0

alpha = 0.01 #learning rate
beta = 0.5 #momentum

X = np.arange(-radius, radius, 1)
Y = np.arange(-radius, radius, 1)

X, Y = np.meshgrid(X, Y)

Z = function(X, Y)

ax = plt.subplot(projection="3d", computed_zorder=False)

facu = Hiker("Facu", current_pos.copy(), radius,"default")

facu.start_strat()

fran = Hiker("Fran", current_pos.copy(), radius,"follow_points")

fran.set_points([-90, 40])

luqui = Hiker("Luqui", current_pos.copy(), radius,"follow_points")

luqui.set_points([-90, -90])

cami = Hiker("Cami", current_pos.copy(), radius,"follow_points")

cami.set_points([0,100])

for _ in range(500):
    print(facu[0:2])
    print(fran[0:2])
    facu.move()

    x, y = facu[0:2]

    dx, dy = dxdy(x, y)

    facu.update_z_dx_dy(-function(x, y), -dx, -dy)
    print(facu[0:2])
    print(fran[0:2])



    fran.move()

    x, y = fran[0:2]

    dx, dy = dxdy(x, y)

    fran.update_z_dx_dy(-function(x, y), -dx, -dy)


    luqui.move()

    x, y = luqui[0:2]

    dx, dy = dxdy(x, y)

    luqui.update_z_dx_dy(-function(x, y), -dx, -dy)


    cami.move()

    x, y = cami[0:2]

    dx, dy = dxdy(x, y)

    cami.update_z_dx_dy(-function(x, y), -dx, -dy)


    print(facu[0:2], "\n", fran[0:2], "\n", luqui[0:2], "\n", cami[0:2], "\n")

    ax.plot_surface(X, Y, Z, cmap="viridis")
    ax.scatter(facu[0], facu[1], -facu[2], color="magenta", zorder=1)
    ax.scatter(fran[0], fran[1], -fran[2], color="red", zorder=1)
    ax.scatter(luqui[0], luqui[1], -luqui[2], color="blue", zorder=1)
    ax.scatter(cami[0], cami[1], -cami[2], color="green", zorder=1)


    plt.pause(0.01)
    ax.clear()

facu.set_points([0/radius, 0/radius])
facu.set_strat("follow_points")

for _ in range(0):
    facu.move()

    x, y = facu[0:2]

    dx, dy = dxdy(x, y)

    facu.update_z_dx_dy(-function(x, y), -dx, -dy)

    ax.plot_surface(X, Y, Z, cmap="viridis")
    ax.scatter(facu[0], facu[1], -facu[2], color="magenta", zorder=1)
    plt.pause(0.01)
    ax.clear()





