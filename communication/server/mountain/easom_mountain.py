"""DO NOT MODIFY THIS FILE"""

import math
from typing import Tuple

from communication.server.mountain.abstract.circularbase_mountain import CircularBaseMountain

class EasomMountain(CircularBaseMountain):
    """Mountain modeled after the Easom function.
    Args:
        visual_radius (float): the radius of the visual area. If the hiker is at least this far from the flag, it will
            be considered that he has reached the flag.
        base_radius (float): the radius of the base of the mountain. If the hiker goes outside this radius, he will be
            considered out of bounds and disqualified.
    """
    def __init__(self, visual_radius: float, base_radius: float) -> None:
        flag = (math.pi,math.pi)
        super().__init__(
            easom_function_creator(), 
            easom_function_gradient_creator(), 
            flag, 
            visual_radius, 
            base_radius,
            (-20, 20),
            (-20, 20)
        )


def easom_function_creator():
    def easom_function(x: float, y: float) -> float:
        ans = -math.cos(x)*math.cos(y)*math.exp(-((x-math.pi)**2 + (y-math.pi)**2))
        return -ans
    return easom_function

def easom_function_gradient_creator():
    def easom_function_gradient_creator(x: float, y: float) -> Tuple[float, float]:
        dfdx = math.exp(-(x-math.pi)**2 - (y-math.pi)**2) * math.cos(y) * (math.sin(x) + 2*(x-math.pi)*math.cos(x))
        dfdy = math.exp(-(x-math.pi)**2 - (y-math.pi)**2) * math.cos(x) * (math.sin(y) + 2*(y-math.pi)*math.cos(y))
        return -dfdx, -dfdy
    return easom_function_gradient_creator