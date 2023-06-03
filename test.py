import math
import matplotlib.pyplot as plt


class MishraBirdMountain:
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

    def mishra_bird_function(self, x: float, y: float) -> float:
        x = x / self.base_radius * 5
        y = y / self.base_radius * 5
        x = x - 5
        y = y - 5
        f = math.sin(y) * math.exp((1 - math.cos(x**2)) ** 2) + math.cos(x) * \
            math.exp((1 - math.sin(y)) ** 2) + (x - y) ** 2 - 100
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

    def plot_mountain(self):
        x = []
        y = []
        z = []

        for i in range(-self.base_radius, self.base_radius + 1):
            for j in range(-self.base_radius, self.base_radius + 1):
                x.append(i)
                y.append(j)
                z.append(self.mishra_bird_function(i, j))

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(x, y, z)
        plt.show()


if __name__ == "__main__":
    mountain = MishraBirdMountain(1, 23)
    mountain.plot_mountain()
