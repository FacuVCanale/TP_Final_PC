import random
import math
from typing import Tuple

from communication.server.mountain.circularbase_mountain import CircularBaseMountain

class RandomMountain(CircularBaseMountain):
    def __init__(self, visual_radius, base_radius) -> None:
        super().__init__(random_function_creator(base_radius), random_gradient_function_creator(base_radius), visual_radius, base_radius)
        self.flag = self.find_global_max()

    def find_global_max(self):
        step = 0.1
        max_value = float('-inf')
        max_point = (0, 0)
        for x in range(-self.base_radius, self.base_radius + 1, step):
            for y in range(-self.base_radius, self.base_radius + 1, step):
                value = self.function(x, y)
                if value > max_value:
                    max_value = value
                    max_point = (x, y)
        return max_point


def random_function_creator(base_radius):
    num_functions = random.randint(1, 5)  # Número aleatorio de funciones que componen la montaña
    functions = []
    for _ in range(num_functions):
        # Generar coeficientes aleatorios para cada función
        coefficients = [random.uniform(-10, 10) for _ in range(6)]
        functions.append(coefficients)
    
    def random_function(x: float, y: float) -> float:
        x = x / base_radius * 5
        y = y / base_radius * 5
        x = x - 5
        y = y - 5
        f = 0
        for coefficients in functions:
            a, b, c, d, e, f_const = coefficients
            f += a * math.sin(b * (x + c)) + d * math.cos(e * (y + f_const))
        return -f

    return random_function


def random_gradient_function_creator(base_radius):
    num_functions = random.randint(1, 5)  # Número aleatorio de funciones que componen la montaña
    functions = []
    for _ in range(num_functions):
        # Generar coeficientes aleatorios para cada función
        coefficients = [random.uniform(-10, 10) for _ in range(6)]
        functions.append(coefficients)
    
    def random_function_gradient(x: float, y: float) -> Tuple[float, float]:
        x = x / base_radius * 5
        y = y / base_radius * 5
        x = x - 5
        y = y - 5
        dfdx = 0
        dfdy = 0
        for coefficients in functions:
            a, b, c, d, e, f_const = coefficients
            dfdx += a * b * math.cos(b * (x + c))
            dfdy += -d * e * math.sin(e * (y + f_const))
        return -dfdx, -dfdy

    return random_function_gradient
