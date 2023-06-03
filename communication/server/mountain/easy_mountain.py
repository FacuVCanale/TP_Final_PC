import math
from typing import Tuple

from communication.server.mountain.circularbase_mountain import CircularBaseMountain

class EasyMountain(CircularBaseMountain):
    def __init__(self, visual_radius, base_radius) -> None:
        flag = [1, 3]
        flag[0] = flag[0] * base_radius /20
        flag[1] = flag[1] * base_radius /20
        flag = tuple(flag)
        super().__init__(booth_function_creator(base_radius), booth_gradient_function_creator(base_radius), flag, visual_radius, base_radius)


def booth_function_creator(base_radius):
    def booth_function(x: float, y: float) -> float:
        x = x / base_radius * 20
        y = y / base_radius * 20
        f = (x+2*y-7)**2 + (2*x+y-5)**2 - 5000
        return -f
    return booth_function

def booth_gradient_function_creator(base_radius):
    def booth_function_gradient(x: float, y: float) -> Tuple[float, float]:
        x = x / base_radius * 20
        y = y / base_radius * 20
        dfdx = 2*(x+2*y-7) + 2*(2*x+y-5)*2
        dfdy = 2*(2*x+y-5) + 2*(x+2*y-7)*2
        return -dfdx, -dfdy
    return booth_function_gradient