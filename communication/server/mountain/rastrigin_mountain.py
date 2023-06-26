"""DO NOT MODIFY THIS FILE"""

import math
from typing import Tuple

from communication.server.mountain.abstract.circularbase_mountain import CircularBaseMountain

class RastriginMountain(CircularBaseMountain):
    """Mountain modeled after the Rastrigin function.
    Args:
        visual_radius (float): the radius of the visual area. If the hiker is at least this far from the flag, it will
            be considered that he has reached the flag.
        base_radius (float): the radius of the base of the mountain. If the hiker goes outside this radius, he will be
            considered out of bounds and disqualified.
    """
    def __init__(self, visual_radius: float, base_radius: float) -> None:
        flag = (0,0)
        super().__init__(
            rastrigin_function_creator(), 
            rastrigin_function_gradient_creator(), 
            flag, 
            visual_radius, 
            base_radius,
            (-5, 5),
            (-5, 5)
        )


def rastrigin_function_creator():
    def rastrigin_function(x: float, y: float) -> float:
        data = [x,y]
        A = 10
        ans = 0
        for i in range(len(data)):
            ans += data[i]**2 - A*math.cos(2*math.pi*data[i])
        ans += A*len(data)
        return -ans + 100
    return rastrigin_function

def rastrigin_function_gradient_creator():
    def rastrigin_function_gradient_creator(x: float, y: float) -> Tuple[float, float]:
        A = 10
        dfdx = 2*(math.pi*A*math.sin(2*math.pi*x) + x)
        dfdy = 2*(y-x) - math.cos(x) * math.exp((1-math.sin(y))**2) * 2 * (1-math.sin(y)) * math.cos(y) + math.cos(y) * math.exp((1-math.cos(x))**2)
        return -dfdx, -dfdy
    return rastrigin_function_gradient_creator