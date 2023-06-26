"""DO NOT MODIFY THIS FILE"""

import math
from typing import Tuple

from communication.server.mountain.abstract.circularbase_mountain import CircularBaseMountain

class AckleyMountain(CircularBaseMountain):
    """Mountain modeled after the Ackley function.
    Args:
        visual_radius (float): the radius of the visual area. If the hiker is at least this far from the flag, it will
            be considered that he has reached the flag.
        base_radius (float): the radius of the base of the mountain. If the hiker goes outside this radius, he will be
            considered out of bounds and disqualified.
    """
    def __init__(self, visual_radius: float, base_radius: float) -> None:
        flag = (0,0)
        super().__init__(
            ackley_function_creator(), 
            ackley_function_gradient_creator(), 
            flag, 
            visual_radius, 
            base_radius,
            (-5, 5),
            (-5, 5)
        )


def ackley_function_creator():
    def ackley_function(x: float, y: float) -> float:
        ans = -20*math.exp(-0.2*math.sqrt(0.5*(x**2 + y**2))) - math.exp(0.5*(math.cos(2*math.pi*x) + math.cos(2*math.pi*y))) + math.e + 20
        return -ans + 20
    return ackley_function

def ackley_function_gradient_creator():
    def ackley_function_gradient_creator(x: float, y: float) -> Tuple[float, float]:
        dfdx = 10*x*math.exp(-0.5*math.sqrt(x**2 + y**2)) / math.sqrt(x**2 + y**2) + math.pi * math.sin(2*math.pi*x) \
            * math.exp(0.5*(math.cos(2*math.pi*x) + math.cos(2*math.pi*y)))
        dfdy = 10*y*math.exp(-0.5*math.sqrt(x**2 + y**2)) / math.sqrt(x**2 + y**2) + math.pi * math.sin(2*math.pi*y) \
            * math.exp(0.5*(math.cos(2*math.pi*x) + math.cos(2*math.pi*y)))
        return -dfdx, -dfdy
    return ackley_function_gradient_creator