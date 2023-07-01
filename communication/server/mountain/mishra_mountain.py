"""DO NOT MODIFY THIS FILE"""

import math
from typing import Tuple

from communication.server.mountain.abstract.circularbase_mountain import CircularBaseMountain

class MishraBirdMountain(CircularBaseMountain):
    """Mountain modeled after the Mishra's Bird function.
    Args:
        visual_radius (float): the radius of the visual area. If the hiker is at least this far from the flag, it will
            be considered that he has reached the flag.
        base_radius (float): the radius of the base of the mountain. If the hiker goes outside this radius, he will be
            considered out of bounds and disqualified.
    """
    def __init__(self, visual_radius: float, base_radius: float) -> None:
        flag = [-3.1302468, -1.5821422]
        super().__init__(
            mishra_bird_function_creator(), 
            mishra_bird_gradient_function_creator(), 
            flag,
            visual_radius, 
            base_radius,
            (-10, 0),
            (-6.5, 0)
        )


def mishra_bird_function_creator():
    def mishra_bird_function(x: float, y: float) -> float:
        f = math.sin(y) * math.exp((1-math.cos(x))**2) + math.cos(x) * math.exp((1-math.sin(y))**2) + (x-y)**2
        return -f + 150
    return mishra_bird_function

def mishra_bird_gradient_function_creator():
    def mishra_bird_function_gradient(x: float, y: float) -> Tuple[float, float]:
        dfdx = 2*(x-y) + math.sin(y) * math.exp((1-math.cos(x))**2) * 2 * (1-math.cos(x)) * math.sin(x) - math.sin(x) * math.exp((1-math.sin(y))**2)
        dfdy = 2*(y-x) - math.cos(x) * math.exp((1-math.sin(y))**2) * 2 * (1-math.sin(y)) * math.cos(y) + math.cos(y) * math.exp((1-math.cos(x))**2)
        return -dfdx, -dfdy
    return mishra_bird_function_gradient