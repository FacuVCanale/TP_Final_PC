import math
from typing import Tuple

from communication.server.mountain.circularbase_mountain import CircularBaseMountain

class MishraBirdMountain(CircularBaseMountain):
    def __init__(self, visual_radius, base_radius) -> None:
        flag = [-3.1302468, -1.5821422]
        flag[0] = flag[0] * base_radius / 5
        flag[1] = flag[1] * base_radius / 5
        flag[0] = flag[0] - 5
        flag[1] = flag[1] - 5
        flag = tuple(flag)
        super().__init__(mishra_bird_function_creator(base_radius), mishra_bird_gradient_function_creator(base_radius), flag, visual_radius, base_radius)


def mishra_bird_function_creator(base_radius):
    def mishra_bird_function(x: float, y: float) -> float:
        x = x / base_radius * 5
        y = y / base_radius * 5
        x = x - 5
        y = y - 5
        f = math.sin(y) * math.exp((1-math.cos(x))**2) + math.cos(x) * math.exp((1-math.sin(y))**2) + (x-y)**2 - 100
        return -f
    return mishra_bird_function

def mishra_bird_gradient_function_creator(base_radius):
    def mishra_bird_function_gradient(x: float, y: float) -> Tuple[float, float]:
        x = x / base_radius * 5
        y = y / base_radius * 5
        x = x - 5
        y = y - 5
        dfdx = 2*(x-y) + math.sin(y) * math.exp((1-math.cos(x))**2) * 2 * (1-math.cos(x)) * math.sin(x) - math.sin(x) * math.exp((1-math.sin(y))**2)
        dfdy = 2*(y-x) - math.cos(x) * math.exp((1-math.sin(y))**2) * 2 * (1-math.sin(y)) * math.cos(y) + math.cos(y) * math.exp((1-math.cos(x))**2)
        return -dfdx, -dfdy
    return mishra_bird_function_gradient