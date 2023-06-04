import math
import random
import matplotlib.pyplot as plt
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
>>>>>>> Stashed changes
import os


class RandomizedMishraBirdMountain:
<<<<<<< Updated upstream
    def __init__(self, visual_radius, base_radius):
        self.visual_radius = visual_radius
        self.base_radius = base_radius
=======
=======
import random


class MishraBirdMountain:
>>>>>>> Stashed changes
    def __init__(self, visual_radius, base_radius):
        flag = [-3.1302468, -1.5821422]
        flag[0] = flag[0] * base_radius / 5
        flag[1] = flag[1] * base_radius / 5
        flag[0] = flag[0] - 5
        flag[1] = flag[1] - 5
        flag = tuple(flag)
        self.flag = flag
        self.visual_radius = visual_radius
        self.base_radius = base_radius
<<<<<<< Updated upstream
>>>>>>> Stashed changes
        self.random_factors = self.generate_random_factors()

    def generate_random_factors(self):
        random_factors = {
            "sin_a": random.uniform(0.5, 2),
            "cos_a": random.uniform(0.5, 2),
            "exp_a": random.uniform(0.5, 2),
            "exp_b": random.uniform(0.5, 2),
            "exp_c": random.uniform(0.5, 2)
        }
        return random_factors
<<<<<<< Updated upstream
=======
=======

        # Agregar variables aleatorias para modificar la montaña
        self.random_radius = random.uniform(0.5, 1.5)
        self.random_offset = random.uniform(-10, 10)
>>>>>>> Stashed changes
>>>>>>> Stashed changes

    def mishra_bird_function(self, x: float, y: float) -> float:
        x = x / self.base_radius * 5
        y = y / self.base_radius * 5
        x = x - 5
        y = y - 5
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
>>>>>>> Stashed changes

        sin_a = self.random_factors["sin_a"]
        cos_a = self.random_factors["cos_a"]
        exp_a = self.random_factors["exp_a"]
        exp_b = self.random_factors["exp_b"]
        exp_c = self.random_factors["exp_c"]

        f = - (math.sin(sin_a * y) * math.exp((1 - math.cos(cos_a * x)) ** exp_a)
               + math.cos(cos_a * x) *
               math.exp((1 - math.sin(sin_a * y)) ** exp_b)
               + (x - y) ** exp_c - 100)

        return f
<<<<<<< Updated upstream
=======
=======
        f = math.sin(y) * math.exp((1 - math.cos(x)) ** 2) + math.cos(x) * \
            math.exp((1 - math.sin(y)) ** 2) + (x - y) ** 2 - 100

        # Agregar variables aleatorias a la función de la montaña
        f += self.random_offset
        f *= self.random_radius

        return -f

    def mishra_bird_function_gradient(self, x: float, y: float) -> tuple:
        x = x / self.base_radius * 5
        y = y / self.base_radius * 5
        x = x - 5
        y = y - 5
        dfdx = 2 * (x - y) + math.sin(y) * math.exp((1 - math.cos(x)) ** 2) * 2 * \
            (1 - math.cos(x)) * math.sin(x) - \
            math.sin(x) * math.exp((1 - math.sin(y)) ** 2)
        dfdy = 2 * (y - x) - math.cos(x) * math.exp((1 - math.sin(y)) ** 2) * 2 * \
            (1 - math.sin(y)) * math.cos(y) + \
            math.cos(y) * math.exp((1 - math.cos(x)) ** 2)
        return -dfdx, -dfdy
>>>>>>> Stashed changes
>>>>>>> Stashed changes

    def plot_mountain(self):
        x = []
        y = []
        z = []

        for i in range(-self.visual_radius, self.visual_radius + 1):
            for j in range(-self.visual_radius, self.visual_radius + 1):
                z_val = self.mishra_bird_function(i, j)
                if isinstance(z_val, complex):
                    continue
                x.append(i)
                y.append(j)
<<<<<<< Updated upstream
                z.append(z_val)
=======
<<<<<<< Updated upstream
                z.append(z_val)
=======
                z.append(self.mishra_bird_function(i, j))
>>>>>>> Stashed changes
>>>>>>> Stashed changes

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(x, y, z)
        plt.show()


if __name__ == "__main__":
<<<<<<< Updated upstream
    os.system("clear")
    mountain = RandomizedMishraBirdMountain(10, 10)
=======
<<<<<<< Updated upstream
    os.system("clear")
    mountain = RandomizedMishraBirdMountain(10, 10)
=======
    mountain = MishraBirdMountain(10, 10)
>>>>>>> Stashed changes
>>>>>>> Stashed changes
    mountain.plot_mountain()
