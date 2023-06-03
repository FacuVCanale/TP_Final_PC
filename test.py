import math
import random
import matplotlib.pyplot as plt
import os


class RandomizedMishraBirdMountain:
    def __init__(self, visual_radius, base_radius):
        self.visual_radius = visual_radius
        self.base_radius = base_radius
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

    def mishra_bird_function(self, x: float, y: float) -> float:
        x = x / self.base_radius * 5
        y = y / self.base_radius * 5
        x = x - 5
        y = y - 5

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
                z.append(z_val)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(x, y, z)
        plt.show()


if __name__ == "__main__":
    os.system("clear")
    mountain = RandomizedMishraBirdMountain(10, 10)
    mountain.plot_mountain()
