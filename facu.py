import math
import random
import matplotlib.pyplot as plt
import os


class RandomizedMountain:
    def __init__(self, visual_radius, base_radius):
        self.visual_radius = visual_radius
        self.base_radius = base_radius
        self.mountain = self.mountain_gen(base_radius)

    def mountain_gen(self, base_radius):
        x = []
        y = []
        z = []
        func = mountain_function_creator(base_radius)

        for i in range(-self.base_radius, self.base_radius + 1):
            for j in range(-self.base_radius, self.base_radius + 1):
                z_val = func(i, j)
                if type(z_val) != int and type(z_val) != float:
                    continue
                x.append(i)
                y.append(j)
                z.append(z_val)
        return [x, y, z]

    def plot_mountain(self):

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(self.mountain[0], self.mountain[1], self.mountain[2])
        plt.show()

def mountain_function_creator(base_radius):
    
    siono = [True, False]

    rango = [-1, 3]

    a = random.uniform(min(rango), max(rango)) if random.choice(siono) else 0
    b = random.uniform(min(rango), max(rango)) if random.choice(siono) else 0
    c = random.uniform(min(rango), max(rango)) if random.choice(siono) else 0
    d = random.uniform(min(rango), max(rango)) if random.choice(siono) else 0
    e = random.uniform(min(rango), max(rango))
    f = random.uniform(min(rango), max(rango))

    def mountain_function(x: float, y: float) -> float:
        val1 = random.uniform(1, 5)

        return math.sin(1/(base_radius/5) * x) * math.cos(1/(base_radius/5) * y) + (1/(base_radius*5))*e*x + (1/(base_radius*5))*f*y
    return mountain_function

if __name__ == "__main__":
    os.system("cls")
    mountain = RandomizedMountain(10, 50)
    mountain.plot_mountain()
