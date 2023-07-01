"""DO NOT MODIFY THIS FILE"""

import math
from typing import Tuple

from communication.server.mountain.abstract.circularbase_mountain import CircularBaseMountain

class SinosidalMountain(CircularBaseMountain):
    """Mountain modeled after the sinosidal function.
    Args:
        visual_radius (float): the radius of the visual area. If the hiker is at least this far from the flag, it will
            be considered that he has reached the flag.
        base_radius (float): the radius of the base of the mountain. If the hiker goes outside this radius, he will be
            considered out of bounds and disqualified.
    """
    def __init__(self, visual_radius: float, base_radius: float) -> None:
        flag = (0,0)
        super().__init__(
            sinosidal_function_creator(), 
            sinosidal_function_gradient_creator(), 
            flag, 
            visual_radius, 
            base_radius,
            (-10, 10),
            (-10, 10)
        )


def sinosidal_function_creator():
    def sinosidal_function(x: float, y: float) -> float:
        if x==0 and y==0:
            return 1
        ans = math.sin(x**2+y**2)/(x**2+y**2)
        return ans
    return sinosidal_function

def sinosidal_function_gradient_creator():
    def sinosidal_function_gradient_creator(x: float, y: float) -> Tuple[float, float]:
        dfdx = 2*x*((x**2+y**2)*math.cos(x**2+y**2)-math.sin(x**2+y**2))/(x**2+y**2)**2
        dfdy = 2*y*((x**2+y**2)*math.cos(x**2+y**2)-math.sin(x**2+y**2))/(x**2+y**2)**2
        return -dfdx, -dfdy
    return sinosidal_function_gradient_creator