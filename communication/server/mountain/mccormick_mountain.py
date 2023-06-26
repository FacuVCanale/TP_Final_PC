"""DO NOT MODIFY THIS FILE"""

import math
from typing import Tuple

from communication.server.mountain.abstract.circularbase_mountain import CircularBaseMountain

class McCormickMountain(CircularBaseMountain):
    """Mountain modeled after the McCormick function.
    Args:
        visual_radius (float): the radius of the visual area. If the hiker is at least this far from the flag, it will
            be considered that he has reached the flag.
        base_radius (float): the radius of the base of the mountain. If the hiker goes outside this radius, he will be
            considered out of bounds and disqualified.
    """
    def __init__(self, visual_radius: float, base_radius: float) -> None:
        flag = [-0.54719, -1.54719]
        super().__init__(
            mccormick_function_creator(),
            mccormick_gradient_function_creator(),
            flag,
            visual_radius,
            base_radius,
            (-1.5, 4),
            (-3, 4)
        )


def mccormick_function_creator():
    def mccormick_function(x: float, y: float) -> float:
        f = math.sin(x+y) + (x-y)**2 - 1.5*x + 2.5*y + 1
        return -f + 100
    return mccormick_function

def mccormick_gradient_function_creator():
    def mccormick_function_gradient(x: float, y: float) -> Tuple[float, float]:
        dfdx = math.cos(x+y) + 2*(x-y) - 1.5
        dfdy = math.cos(x+y) - 2*(x-y) + 2.5
        return -dfdx, -dfdy
    return mccormick_function_gradient