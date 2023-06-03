import random
import math
import matplotlib.pyplot as plt


class RandomMountain:
    def __init__(self, visual_radius, base_radius):
        self.visual_radius = visual_radius
        self.base_radius = base_radius
        self.functions = [
            lambda x, y: x**2 + y**2,
            lambda x, y: x**3 + y**3,
            lambda x, y: math.sin(x) + math.cos(y),
            lambda x, y: math.exp(x) - math.exp(y)
        ]

    def random_mountain_function(self):
        num_functions = random.randint(1, len(self.functions))
        selected_functions = random.sample(self.functions, num_functions)
        scalars = [random.uniform(0.5, 2.0) for _ in range(num_functions)]

        def mountain_function(x, y):
            result = 0
            for func, scalar in zip(selected_functions, scalars):
                result += scalar * func(x, y)
            return result

        return mountain_function

    def plot_mountain(self):
        x = []
        y = []
        z = []

        mountain_function = self.random_mountain_function()

        for i in range(-self.visual_radius, self.visual_radius + 1):
            for j in range(-self.visual_radius, self.visual_radius + 1):
                x.append(i)
                y.append(j)
                z.append(mountain_function(i, j))

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(x, y, z)
        plt.show()


if __name__ == "__main__":
    mountain = RandomMountain(10, 10)
    mountain.plot_mountain()
