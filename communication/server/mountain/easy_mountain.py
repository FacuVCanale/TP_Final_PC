"""DO NOT MODIFY THIS FILE"""

from typing import Tuple

from communication.server.mountain.abstract.circularbase_mountain import CircularBaseMountain

class EasyMountain(CircularBaseMountain):
    """Mountain modeled after the Booth function.
    Args:
        visual_radius (float): the radius of the visual area. If the hiker is at least this far from the flag, it will
            be considered that he has reached the flag.
        base_radius (float): the radius of the base of the mountain. If the hiker goes outside this radius, he will be
            considered out of bounds and disqualified.
    """
    def __init__(self, visual_radius: float, base_radius: float) -> None:
        flag = [1, 3]
        super().__init__(
            booth_function_creator(),
            booth_gradient_function_creator(),
            flag,
            visual_radius, 
            base_radius,
            (-10, 10),
            (-10, 10)    
        )


def booth_function_creator():
    def booth_function(x: float, y: float) -> float:
        f = (x+2*y-7)**2 + (2*x+y-5)**2
        return -f + 2000
    return booth_function

def booth_gradient_function_creator():
    def booth_function_gradient(x: float, y: float) -> Tuple[float, float]:
        dfdx = 2*(x+2*y-7) + 2*(2*x+y-5)*2
        dfdy = 2*(2*x+y-5) + 2*(x+2*y-7)*2
        return -dfdx, -dfdy
    return booth_function_gradient