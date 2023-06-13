import math
from typing import Tuple

from communication.server.mountain.circularbase_mountain import CircularBaseMountain

class McCormickMountain(CircularBaseMountain):
    def __init__(self, visual_radius, base_radius) -> None:
        flag = [-0.54719, -1.54719]
        flag[0] = flag[0] * base_radius / 5.5
        flag[1] = flag[1] * base_radius / 7
        flag = tuple(flag)
        super().__init__(mccormick_function_creator(base_radius), mccormick_gradient_function_creator(base_radius), flag, visual_radius, base_radius)


def mccormick_function_creator(base_radius):
    def mccormick_function(x: float, y: float) -> float:
        x_range = (-1.5, 4)
        y_range = (-3, 4)
        x = x / base_radius * 5.5
        y = y / base_radius * 7
        x += (x_range[1] + x_range[0]) / 2
        y += (y_range[1] + y_range[0]) / 2
        f = math.sin(x+y) + (x-y)**2 - 1.5*x + 2.5*y - 70
        return -f
    return mccormick_function

def mccormick_gradient_function_creator(base_radius):
    def mccormick_function_gradient(x: float, y: float) -> Tuple[float, float]:
        x = x / base_radius * 5.5
        y = y / base_radius * 7
        dfdx = math.cos(x+y) + 2*(x-y) - 1.5
        dfdy = math.cos(x+y) - 2*(x-y) + 2.5
        return -dfdx, -dfdy
    return mccormick_function_gradient